import logging
from typing import Generator, Union
from spaceone.core.manager import BaseManager
from spaceone.core.connector.space_connector import SpaceConnector

__ALL__ = ["CollectorPluginManager"]

_LOGGER = logging.getLogger(__name__)


class CollectorPluginManager(BaseManager):
    def init_plugin(self, endpoint: str, options: dict) -> dict:
        plugin_connector: SpaceConnector = self.locator.get_connector(
            SpaceConnector, endpoint=endpoint, token="NO_TOKEN"
        )
        return plugin_connector.dispatch("Collector.init", {"options": options})

    def verify_plugin(self, endpoint: str, options: dict, secret_data: dict) -> None:
        plugin_connector: SpaceConnector = self.locator.get_connector(
            SpaceConnector, endpoint=endpoint, token="NO_TOKEN"
        )
        params = {"options": options, "secret_data": secret_data}
        plugin_connector.dispatch("Collector.verify", params)

    def collect(
        self,
        endpoint: str,
        options: dict,
        secret_data: dict,
        task_options: dict = None,
    ) -> Generator[dict, None, None]:
        collector_version = task_options.get("collector_version", "v1")

        if collector_version == "v1":
            plugin_connector =
        else:


    def get_tasks(self, endpoint: str, secret_data: dict, options: dict) -> dict:
        plugin_connector: SpaceConnector = self.locator.get_connector(
            SpaceConnector, endpoint=endpoint, token="NO_TOKEN"
        )

        params = {"options": options, "secret_data": secret_data}
        return plugin_connector.dispatch("Job.get_tasks", params)
