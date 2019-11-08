from starlette.requests import Request
from starlette.responses import Response

from directus.application import app
from directus.upstream import get_upstream_raw_response


@app.middleware("http")
async def pass_to_upstream(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        raw = await get_upstream_raw_response(request)
        response = Response(raw.content, status_code=raw.status_code, headers=raw.headers)
    return response
