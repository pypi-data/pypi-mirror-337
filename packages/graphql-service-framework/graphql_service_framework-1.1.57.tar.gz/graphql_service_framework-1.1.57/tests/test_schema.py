import pytest
import datetime

from typing import Optional, Dict

from context_helper import ctx
from graphql_api import field
from schemadiff.changes import CriticalityLevel
from werkzeug.test import Client

from graphql_http_server import GraphQLHTTPServer

from graphql_service_framework.schema import Schema
from tests.utils import available


# noinspection DuplicatedCode
class TestSchema:
    def test_schema_validation(self):
        from graphql_api import GraphQLAPI

        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            @field
            def now(self) -> Optional[str]:
                return str(datetime.datetime.now())

        server = GraphQLHTTPServer.from_api(api=GraphQLAPI(root_type=UTCTimeService))

        client = Client(server.app())

        response = client.get("/?query={now}")

        assert response.status_code == 200
        assert "now" in response.text

        class InvalidUTCTimeService(UTCTime):
            @field
            def now(self) -> str:
                return str(datetime.datetime.now())

        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.validate_schema = False
        assert GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.validate_schema = True
        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.criticality = CriticalityLevel.Breaking

        assert GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

    @pytest.mark.skip
    def test_schema_no_field(self):
        from graphql_api import GraphQLAPI

        class HelloSchema(Schema):

            def hello(self) -> str:
                raise NotImplementedError()

        class HelloService(HelloSchema):

            def hello(self) -> str:
                return "Hello User"

        server = GraphQLHTTPServer.from_api(api=GraphQLAPI(root_type=HelloService))

        client = Client(server.app())

        response = client.get("/?query={hello}")

        assert response.status_code == 200
        assert "Hello User" in response.text

    def test_schema_validation_no_field(self):
        from graphql_api import GraphQLAPI

        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            def now(self) -> Optional[str]:
                return str(datetime.datetime.now())

        server = GraphQLHTTPServer.from_api(api=GraphQLAPI(root_type=UTCTimeService))

        client = Client(server.app())

        response = client.get("/?query={now}")

        assert response.status_code == 200
        assert "now" in response.text

        class InvalidUTCTimeService(UTCTime):
            def now(self) -> str:
                return str(datetime.datetime.now())

        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.validate_schema = False
        assert GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.validate_schema = True
        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

        InvalidUTCTimeService.criticality = CriticalityLevel.Breaking

        assert GraphQLAPI(root_type=InvalidUTCTimeService).build_schema()

    def test_schema_client(self):
        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            @field
            def now(self) -> Optional[str]:
                return str(datetime.datetime.now())

        with pytest.raises(ValueError):
            client = UTCTime()
            assert client

        client = UTCTime(url="http://invalid_url.test")
        assert client

        with pytest.raises(Exception, match="Cannot connect to host"):
            _ = client.now()

        local_client = UTCTimeService()
        assert local_client.now()

    def test_create_service(self):
        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            @field
            def now(self) -> Optional[str]:
                return str(datetime.datetime.now())

        service = UTCTimeService(config={"test": "test"}).create_service()

        assert service

    def test_create_service_init(self):
        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            def __init__(self, offset: int, config: Dict = None):
                super().__init__(config=config)
                self.offset = offset

            @field
            def now(self) -> Optional[str]:
                return str(
                    datetime.datetime.now() + datetime.timedelta(seconds=self.offset)
                )

        service = UTCTimeService(offset=1, config={"test": "test"}).create_service()

        client = service.client()

        response = client.get("?query={now}")

        assert response.status_code == 200 and "now" in response.text

    def test_service_schema(self):
        class UTCTime(Schema, schema_version="1.2.3"):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):
            def __init__(self, offset: int, config: Dict = None):
                super().__init__(config=config)
                self.offset = offset

            @field
            def now(self) -> Optional[str]:
                return str(
                    datetime.datetime.now() + datetime.timedelta(seconds=self.offset)
                )

        service = UTCTimeService(offset=1, config={"test": "test"}).create_service()

        client = service.client()

        response = client.get("/service?query={schemaVersion, serviceVersion}")

        assert (
            response.status_code == 200
            and response.text == '{"data":{"schemaVersion":"1.2.3"'
            ',"serviceVersion":"0.0.0.dev"}}'
        )

    utc_time_api_url = (
        "https://europe-west2-parob-297412.cloudfunctions." "net/utc_time"
    )

    # noinspection DuplicatedCode,PyUnusedLocal
    @pytest.mark.skipif(
        not available(utc_time_api_url),
        reason=f"The UTCTime API '{utc_time_api_url}' is unavailable",
    )
    def test_create_service_mesh(self):
        class UTCTime(Schema):
            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class TimeOffset(Schema):
            @field
            def now(self, offset: int) -> Optional[str]:
                raise NotImplementedError()

        class TimeOffsetService(TimeOffset):
            @field
            def now(self, offset: int) -> Optional[str]:
                utc_time: UTCTime = ctx.services.utc_time
                now = datetime.datetime.fromisoformat(utc_time.now())
                return str(now + datetime.timedelta(seconds=offset))

        service = TimeOffsetService(
            config={
                "services": {
                    "utc_time": UTCTime(
                        url="https://europe-west2-parob-297412.cloudfunctions.net/"
                        "utc_time"
                    )
                }
            }
        ).create_service()

        client = service.client()

        response = client.get("?query={now(offset:7200)}")
        assert response

    def test_federated_service(self):

        class Timezone:
            @field
            def name(self) -> str:
                raise NotImplementedError()

        class UTCTime(Schema, schema_version="1.2.3", federation=True):

            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

            @field
            def timezones(self) -> Timezone:
                raise NotImplementedError()

        # noinspection PyRedeclaration
        class Timezone(Timezone):
            @field
            def name(self) -> str:
                return "UTC"

        class UTCTimeService(UTCTime):
            def __init__(self, offset: int, config: Dict = None):
                super().__init__(config=config)
                self.offset = offset

            @field
            def now(self) -> Optional[str]:
                return str(
                    datetime.datetime.now() + datetime.timedelta(seconds=self.offset)
                )

            @field
            def timezones(self) -> Timezone:
                raise NotImplementedError()

        service = UTCTimeService(offset=1, config={"test": "test"}).create_service()

        client = service.client()

        response = client.get("/service?query={schemaVersion, serviceVersion}")

        assert (
            response.status_code == 200
            and response.text == '{"data":{"schemaVersion":"1.2.3"'
            ',"serviceVersion":"0.0.0.dev"}}'
        )
