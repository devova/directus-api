from json import JSONDecodeError

import httpx
from fastapi import Depends
from httpx import URL as xURL
from starlette.datastructures import URL
from starlette.requests import Request

from directus.application import app


async def get_upstream_raw_response(request: Request):
    config = app.extra['config']
    async with httpx.AsyncClient(http_versions=['HTTP/1.1']) as client:
        upstream_url = URL(config.upstream.url)
        url = request.url.replace(netloc=upstream_url.netloc, path=(upstream_url.path.rstrip('/')+request.url.path))
        url = xURL(str(url))
        body = await request.body()
        return await client.request(
            request.method, url, data=body, headers=request.headers.raw, cookies=request.cookies, allow_redirects=False)


UpstreamRawResponse = Depends(get_upstream_raw_response)


async def get_upstream_response(request: Request):
    upstream_raw_response = await get_upstream_raw_response(request)
    if upstream_raw_response.status_code < 300:
        try:
            return upstream_raw_response.json()
        except JSONDecodeError:
            pass

UpstreamResponse = Depends(get_upstream_response)
