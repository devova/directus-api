from starlette.requests import Request

import collections
from directus.application import app
from directus.upstream import get_upstream_response


@app.get("/_/fields/{collection}")
async def endpoint(request: Request, collection: str):
    if collection not in collections.REGISTRY:
        return await get_upstream_response(request)
    return {
        'data': collections.REGISTRY[collection].fields_info()
    }
