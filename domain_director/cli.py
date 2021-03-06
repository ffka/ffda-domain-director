import os

import click as click
import yaml
from waitress import serve

from domain_director.server import create_app


def read_config_file(path):
    with open(path, "r") as f:
        content = f.read()
        config = yaml.load(content)
        return config


@click.command()
@click.option('--config', default='config.yml', help='Host of web-server.')
def run(config):
    config_file_path = os.path.join(os.getcwd(), config) if config[0] != os.sep else config
    app_config = read_config_file(config_file_path)

    geojson_file_path = os.path.join(os.getcwd(), app_config["geojson"]) if app_config["geojson"][0] != os.sep else \
        app_config["geojson"]

    app = create_app(dict(
        GEOJSON_FILE=geojson_file_path,
        MLS_API_KEY=app_config["mls_api_key"],
        DOMAIN_SWITCH_TIME=app_config["domain_switch_time"],
        DEFAULT_DOMAIN=app_config["default_domain"],
        MESHVIEWER_JSON_URL=app_config["meshviewer_json_url"],
        SQLITE_PATH=app_config["sqlite_path"],
        UPDATE_INTERVAL=app_config["update_interval"],
        ONLY_MIGRATE_VPN=app_config["only_migrate_vpn"]
    ))
    serve(app, listen='{host}:{port}'.format(host=app_config["host"], port=app_config["port"]))
