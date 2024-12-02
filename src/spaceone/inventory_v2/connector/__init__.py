from spaceone.core.connector import BaseConnector

from spaceone.inventory_v2.connector.collector_plugin_v1_connector import (
    CollectorPluginV2Connector,
    CollectorPluginV1Connector,
)


class BaseCollectorPluginConnector(BaseConnector):
    collector_version = "v1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        endpoint = kwargs.get("endpoint")
        plugin_connector: SpaceConnector = self.locator.get_connector(
            SpaceConnector, endpoint=endpoint, token="NO_TOKEN"
        )

        params = {"options": options, "secret_data": secret_data, "filter": {}}

        if task_options:
            params["task_options"] = task_options

        return plugin_connector.dispatch("Collector.collect", params)

    @classmethod
    def get_connector_by_collector_version(cls, collector_version: str):
        if collector_version == "v2":
            return CollectorPluginV2Connector
        else:
            return CollectorPluginV1Connector
