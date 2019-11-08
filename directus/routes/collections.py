import collections
from directus.application import app
from directus.upstream import UpstreamResponse


@app.get("/_/collections")
async def read_root(upstream_response: dict = UpstreamResponse):
    if not upstream_response:
        upstream_response = {'data': []}
    for c in collections.REGISTRY.values():
        upstream_response['data'].append(c.info())
    return upstream_response
