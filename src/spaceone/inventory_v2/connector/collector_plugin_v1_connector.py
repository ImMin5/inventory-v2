from spaceone.core.connector import BaseConnector

from spaceone.inventory_v2.connector import BaseCollectorPluginConnector


class CollectorPluginV1Connector(BaseCollectorPluginConnector):
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

    def collect(self, params):
        return self.grpc_client.Collector.collect(params)


class CollectorPluginV2Connector(B)
