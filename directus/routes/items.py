from fastapi import Body
from starlette.requests import Request
from starlette.responses import Response

import directus.collections as collections
import directus.collections.registry
from directus.application import app
from directus.upstream import get_upstream_response


@app.get("/_/items/{collection}")
async def endpoint(request: Request, collection: str):
    if collection not in directus.collections.registry.REGISTRY:
        return await get_upstream_response(request)
    items = directus.collections.registry.REGISTRY[collection].items(request.scope)
    return {
        'data': items,
        'meta': {
            'result_count': len(items),
            'total_count': len(items)
        }
    }


@app.post("/_/items/{collection}")
async def endpoint(request: Request, collection: str, data: dict = Body({})):
    if collection not in directus.collections.registry.REGISTRY:
        return await get_upstream_response(request)
    return {
        'data': directus.collections.registry.REGISTRY[collection].create(data)
    }


@app.get("/_/items/{collection}/{id}")
async def endpoint(request: Request, collection: str, id: int):
    if collection not in directus.collections.registry.REGISTRY:
        return await get_upstream_response(request)
    return {
        'data': directus.collections.registry.REGISTRY[collection].get(id)
    }


@app.patch("/_/items/{collection}/{id}")
async def endpoint(request: Request, collection: str, id: int, data: dict = Body({})):
    if collection not in directus.collections.registry.REGISTRY:
        return await get_upstream_response(request)
    return {
        'data': directus.collections.registry.REGISTRY[collection].update(id, data)
    }


@app.delete("/_/items/{collection}/{id}")
async def endpoint(request: Request, collection: str, id: int):
    if collection not in directus.collections.registry.REGISTRY:
        return await get_upstream_response(request)
    deleted = directus.collections.registry.REGISTRY[collection].delete(id)
    if deleted:
        return Response(status_code=204)
    return Response(status_code=404)
