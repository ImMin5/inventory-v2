import logging
from typing import Union, Tuple, List

from spaceone.core.model.mongo_model import QuerySet
from spaceone.core.manager import BaseManager
from spaceone.inventory_v2.model.collection_state.database import CollectionState

_LOGGER = logging.getLogger(__name__)


class CollectionStateManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector_id = self.transaction.get_meta("collector_id")
        self.job_task_id = self.transaction.get_meta("job_task_id")
        self.secret_id = self.transaction.get_meta("secret.secret_id")
        self.collection_state_model = CollectionState

    def create_collection_state(self, asset_id: str, domain_id: str) -> None:
        def _rollback(vo: CollectionState):
            _LOGGER.info(
                f"[ROLLBACK] Delete collection state: asset_id = {vo.asset_id}, "
                f"collector_id = {vo.collector_id}"
            )
            vo.terminate()

        if self.collector_id and self.job_task_id and self.secret_id:
            state_data = {
                "collector_id": self.collector_id,
                "job_task_id": self.job_task_id,
                "secret_id": self.secret_id,
                "asset_id": asset_id,
                "domain_id": domain_id,
            }

            state_vo = self.collection_state_model.create(state_data)
            self.transaction.add_rollback(_rollback, state_vo)

    def update_collection_state_by_vo(
        self, params: dict, state_vo: CollectionState
    ) -> CollectionState:
        def _rollback(old_data):
            _LOGGER.info(
                f"[ROLLBACK] Revert collection state : asset_id = {state_vo.asset_id}, "
                f"collector_id = {state_vo.collector_id}"
            )
            state_vo.update(old_data)

        self.transaction.add_rollback(_rollback, state_vo.to_dict())
        return state_vo.update(params)

    def reset_collection_state(self, state_vo: CollectionState) -> None:
        if self.job_task_id:
            params = {"disconnected_count": 0, "job_task_id": self.job_task_id}

            self.update_collection_state_by_vo(params, state_vo)

    def get_collection_state(
        self, asset_id: str, domain_id: str
    ) -> Union[CollectionState, None]:
        if self.collector_id and self.secret_id:
            state_vos = self.collection_state_model.filter(
                collector_id=self.collector_id,
                secret_id=self.secret_id,
                asset_id=asset_id,
                domain_id=domain_id,
            )

            if state_vos.count() > 0:
                return state_vos[0]

        return None

    def filter_collection_states(self, **conditions) -> QuerySet:
        return self.collection_state_model.filter(**conditions)

    def list_collection_states(self, query: dict) -> Tuple[QuerySet, int]:
        return self.collection_state_model.query(**query)

    def delete_collection_state_by_asset_id(
        self, resource_id: str, domain_id: str
    ) -> None:
        state_vos = self.filter_collection_states(
            asset_id=resource_id, domain_id=domain_id
        )
        state_vos.delete()

    def delete_collection_state_by_asset_ids(self, asset_ids: List[str]) -> None:
        state_vos = self.filter_collection_states(asset_id=asset_ids)
        state_vos.delete()

    def delete_collection_state_by_collector_id(
        self, collector_id: str, domain_id: str
    ) -> None:
        state_vos = self.filter_collection_states(
            collector_id=collector_id, domain_id=domain_id
        )
        state_vos.delete()
