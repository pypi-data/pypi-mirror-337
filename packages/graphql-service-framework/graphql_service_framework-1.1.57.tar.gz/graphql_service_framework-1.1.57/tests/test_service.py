from unittest import mock
from unittest.mock import ANY

import pytest
from graphql_api import field
from starlette.datastructures import Headers
from starlette.testclient import TestClient

from graphql_service_framework import Schema
from graphql_service_framework.service import GraphQLService
from tests.utils import BasicService


class TestService:
    @mock.patch("graphql_http_server.GraphQLHTTPServer.from_api")
    def test_create_graphql_service_config(self, mock_from_api):
        root = BasicService(hello_response="service_ab")
        config = {
            "graphiql_default": "./.graphql",
            "service_manager_path": "/test_service",
        }
        GraphQLService(root, config=config)

        mock_from_api.assert_any_call(
            api=ANY,
            root_value=root,
            graphiql_default_query="./.graphql",
            health_path="/health",
            allow_cors=True,
            auth_domain=None,
            auth_audience=None,
            auth_enabled=False,
        )

        config = {
            "graphiql_default": "./.graphql",
            "auth": {
                "enabled": "true",
                "domain": "https://auth.com",
                "audience": "myapp",
            },
        }

        GraphQLService(root, config=config)

        mock_from_api.assert_any_call(
            api=ANY,
            root_value=root,
            graphiql_default_query="./.graphql",
            health_path="/health",
            allow_cors=True,
            auth_domain="https://auth.com",
            auth_audience="myapp",
            auth_enabled=True,
        )

        config = {
            "graphiql_default": "./.graphql",
            "auth": {"enabled": "true", "audience": "myapp"},
        }

        with pytest.raises(KeyError):
            GraphQLService(root, config=config)

        config = {
            "graphiql_default": "./.graphql",
            "auth": {"enabled": "true", "domain": "https://auth.com"},
        }

        with pytest.raises(KeyError):
            GraphQLService(root, config=config)

    def test_service_graphql_middleware(self):

        class HelloWorldSchema(Schema, schema_version="4.5.6"):
            @field
            def hello(self) -> str:
                raise NotImplementedError()

        class HelloWorld(HelloWorldSchema):

            @field
            def hello(self) -> str:
                return "hello"

        def auth_middleware(next_, info, root, **args):
            value = next_(info, root, **args)
            return value + " world"

        service = HelloWorld(config={"middleware": [auth_middleware]}).create_service()

        client = service.client()
        response = client.get("/?query={hello}")

        assert response.status_code == 200
        assert response.json() == {"data": {"hello": "hello world"}}

    def test_service_http_api_key_middleware(self):

        class CalculatorSchema(Schema, schema_version="4.5.6"):
            @field
            def add(self, a: int, b: int) -> int:
                raise NotImplementedError()

        class Calculator(CalculatorSchema):

            @field
            def add(self, a: int, b: int) -> int:
                return a + b

        calculator_service = Calculator().create_service()
        calculator_asgi_app = calculator_service.create_asgi_app()

        class BasicApiKeyMiddleware:
            def __init__(self, app, api_key):
                self.app = app
                self.api_key = api_key

            async def __call__(self, scope, receive, send):
                api_key = Headers(raw=scope["headers"]).get("API_KEY")
                if not api_key or api_key != self.api_key:
                    await send({"type": "http.response.start", "status": 401})
                else:
                    await self.app(scope, receive, send)

        auth_asgi_app = BasicApiKeyMiddleware(calculator_asgi_app, api_key="rn34f3")

        client = TestClient(auth_asgi_app)

        response_1 = client.get("/?query={add(a:1, b:5)}")
        assert response_1.status_code == 401

        response_2 = client.get("/?query={add(a:1, b:5)}", headers={"API_KEY": "1234"})
        assert response_2.status_code == 401

        response_3 = client.get(
            "/?query={add(a:1, b:5)}", headers={"API_KEY": "rn34f3"}
        )
        assert response_3.status_code == 200
        assert response_3.json() == {"data": {"add": 6}}
