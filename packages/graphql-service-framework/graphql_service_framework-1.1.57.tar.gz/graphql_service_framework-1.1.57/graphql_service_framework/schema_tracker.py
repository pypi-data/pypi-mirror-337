import functools
import importlib
import inspect
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Type, List

from graphql import print_schema

from schemadiff import diff
from schemadiff.formatting import format_change_by_criticality

from graphql_service_framework.schema import Schema
from graphql_service_framework.utils import (
    increment_version,
    install_package,
    find_modules,
    find_schema,
    get_py_code_changes,
    set_schema_version,
)


@dataclass
class SchemaChangeTracker:
    name: str
    path: str
    schema: Type[Schema]

    @classmethod
    def find_schemas(
        cls, path, schemas_package_name, index_url, suffix=None
    ) -> List["SchemaChangeTracker"]:
        print(
            f"* Searching for schema directories in {path} with "
            f"package name {schemas_package_name}"
        )
        schema_change_trackers = []
        for folder in os.listdir(path):
            full_path = os.path.join(path, folder)
            if (
                os.path.isdir(full_path)
                and not folder.startswith(".")
                and folder not in ["tests"]
            ):
                schema_name = folder

                if modules := find_modules(full_path, schema_name):
                    if schema := find_schema(modules):
                        schema_change_trackers.append(
                            SchemaChangeTracker(
                                name=schema_name,
                                path=full_path,
                                schema=schema,
                                schemas_package_name=schemas_package_name,
                                index_url=index_url,
                                suffix=suffix,
                            )
                        )

        return schema_change_trackers

    def __init__(
        self,
        schema: Type[Schema],
        name: str,
        path: str,
        schemas_package_name: str,
        index_url: str,
        suffix: str = None,
        dev: bool = False,
    ):
        self.schema = schema
        self.name = name
        self.path = path
        self.suffix = suffix
        self.schemas_package_name = schemas_package_name
        self.index_url = index_url

    def package_name(self):
        return (self.name + f"_{self.suffix}").replace("-", "_")

    def __hash__(self):
        return hash((self.name, self.path))

    @functools.cache
    def previous_schema(self) -> Optional[Type[Schema]]:
        # noinspection PyBroadException
        print(f"Checking for a previous version of {self.package_name()}")
        prev_report = install_package(self.package_name(), index_url=self.index_url)

        if prev_report:
            v = prev_report["install"][0]["metadata"]["version"]

            install_location = prev_report.get("pip_show").get("Location")
            print(
                f"Installed package "
                f"{self.package_name()} version {v} at "
                f"{install_location}"
            )
            schema = None
            err = None
            try:
                location = os.path.join(
                    install_location, self.schemas_package_name, self.name
                )
                module_name = f"{self.schemas_package_name}.{self.name}"
                prev_modules = find_modules(
                    location,
                    module_name,
                )
                if not prev_modules:
                    raise TypeError(
                        f"Could not find any modules in {location} with module "
                        f"name {module_name}"
                    )

                schema = find_schema(prev_modules)
                print(
                    f"Found previous version of {self.package_name()}. Schema {schema}"
                    f" version {schema.schema_version}"
                )
                return schema
            except Exception as _err:
                err = _err

            if not schema:
                raise TypeError(
                    f"Managed to install package {self.package_name()} but unable to "
                    f"find previous schema {self.package_name()} from version {v} {err}"
                )
        else:
            return None

    @functools.cache
    def code_changes(self):
        if self.previous_schema():
            b_module = importlib.import_module(
                f"{self.schemas_package_name}.{self.name}"
            )

            if not b_module:
                raise TypeError(
                    f"Unable to import {self.schemas_package_name}.{self.name}"
                )
            if b_module and not b_module.__file__:
                raise TypeError(
                    f"Unable to import {self.schemas_package_name}.{self.name}."
                    f"Possibly missing a __init__.py file from this schemas package."
                )

            a_path = self.path
            b_path = os.path.dirname(b_module.__file__)

            print(
                f"Comparing code for {self.package_name()} with version "
                f"{self.previous_schema().schema_version}\n"
                f"a_path={a_path}\nb_path={b_path}"
            )
            return get_py_code_changes(
                a_path, b_path, self.previous_schema().schema_version
            )
        return None

    def changes(self):
        if not self.previous_schema():
            return []
        else:
            new_schema_language = print_schema(self.schema.graphql_schema())
            previous_schema_language = print_schema(
                self.previous_schema().graphql_schema()
            ).replace(f"{self.schemas_package_name}.", "")

            return diff(previous_schema_language, new_schema_language)

    def change_log(self, developmental_release=None, force_release=False):
        new_version = self.generate_new_version(
            developmental_release=developmental_release, force_release=force_release
        )
        prev_version = (
            self.previous_schema().schema_version if self.previous_schema() else None
        )

        version = (
            f"**{new_version}** (updated from *{prev_version}*)"
            if prev_version and prev_version != new_version
            else f"*{new_version}*"
        )

        log = f"- {self.package_name()} {version}\n"
        if not self.previous_schema():
            log += "  - *New Schema*\n"
        elif not self.changes() and self.code_changes():
            log += "  - *Code changes only* (No Schema changes)\n"
        elif (
            self.major_changes_count()
            or self.minor_changes_count()
            or self.micro_changes_count()
        ):
            log += (
                f"  - "
                f"{self.major_changes_count()} breaking, "
                f"{self.minor_changes_count()} safe, "
                f"{self.micro_changes_count()} micro Schema changes \n"
            )
            for change in self.changes():
                log += f"    - {format_change_by_criticality(change)}\n"

        return log

    def major_changes_count(self):
        return sum(change.breaking or change.dangerous for change in self.changes())

    def minor_changes_count(self):
        return sum(
            change.safe and "DescriptionChanged" not in change.__class__.__name__
            for change in self.changes()
        )

    def micro_changes_count(self):
        count = sum(
            "DescriptionChanged" in change.__class__.__name__
            for change in self.changes()
        )
        if (
            not count
            and (not self.minor_changes_count() or not self.major_changes_count())
            and (self.code_changes() or not self.previous_schema())
        ):
            count = 1

        return count

    def generate_new_version(self, developmental_release=None, force_release=False):
        new_version = "0.0.1"

        if not self.previous_schema():
            previous_version = "0.0.1"
        else:
            previous_version = self.previous_schema().schema_version

            if self.major_changes_count():
                new_version = increment_version(previous_version, 0)
            elif self.minor_changes_count():
                new_version = increment_version(previous_version, 1)
            elif self.micro_changes_count() or force_release:
                new_version = increment_version(previous_version, 2)

        if developmental_release:
            new_version = f"{previous_version}.{developmental_release}"
        return new_version

    def release(self, developmental_release=None, force_release=False):
        new_version = self.generate_new_version(
            developmental_release=developmental_release, force_release=force_release
        )
        if not self.previous_schema():
            previous_version = "0.0.1"
        else:
            previous_version = self.previous_schema().schema_version

        release_reason = None
        if not self.previous_schema():
            release_reason = "this is a new schema"
        elif self.changes():
            release_reason = "the schema has been changed"
        elif self.code_changes():
            release_reason = "the source code as been changed"
        elif force_release:
            release_reason = "the release has been forced."
        elif developmental_release:
            release_reason = "this is a developmental release."

        if not release_reason:
            print(f"Not releasing {self.package_name()}, no reason to release.")
            return

        print(f"Releasing {self.package_name()} because {release_reason}")
        print(f"{self.package_name()} version {previous_version} -> {new_version}")
        print(f"Creating setup.py in {self.path} for {self.package_name()}")

        setup_data = (
            inspect.cleandoc(
                """
            from setuptools import setup, find_namespace_packages

            setup(
                name='SERVICE_NAME',
                version='SERVICE_VERSION',
                packages=find_namespace_packages(include=[
                    'SERVICE_PACKAGE',
                    'SERVICE_PACKAGE.*'
                ]),
                install_requires=[
                    'packaging',
                    'graphql-service-framework'
                ]
            )
            """
            )
            .replace(
                "SERVICE_NAME",
                self.package_name(),
            )
            .replace("SERVICE_VERSION", new_version)
            .replace("SERVICE_PACKAGE", f"{self.schemas_package_name}.{self.name}")
        )

        with open(os.path.join(self.path, "setup.py"), "w") as file:
            file.write(setup_data)

        print(f"Inserting schema_version = {new_version} into {self.package_name()}")
        for file in Path(self.path).rglob("*.py"):
            file.write_text(set_schema_version(file.read_text(), new_version))
