# -*- coding: utf-8 -*-

from unittest import TestCase

from starlette.testclient import TestClient

from core_apis.api import create_application


class BaseApiTestCases(TestCase):
    """ Base class for tests related to the API """
    
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.init_client()

    @classmethod
    def init_client(cls, with_cors: bool = True):
        app = create_application(name="API-Tests", add_cors_middleware=with_cors)
        cls.client = TestClient(app)
        cls.app = app
