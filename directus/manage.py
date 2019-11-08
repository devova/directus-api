import hydra

from directus.middlewares import *  # noqa
from directus.routes import *  # noqa
from directus.application import app


@hydra.main(config_path='config.yaml')
def run(cfg):
    app.extra['config'] = cfg

    import uvicorn
    uvicorn.run(app, host=cfg.server.host, port=cfg.server.port, reload=True)


# this function is required to allow automatic detection of the module name when running
# from a binary script.
# it should be called from the executable script and not the hydra.main() function directly.
def entry():
    run()
