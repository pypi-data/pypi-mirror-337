# -*- coding: utf-8 -*-

from typing import List

from fastapi import APIRouter


# Inject the routers...
routers: List[APIRouter] = []


def add_router(router: APIRouter):
    routers.append(router)
