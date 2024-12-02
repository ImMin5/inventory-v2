from mongoengine import *
from datetime import datetime

from spaceone.core.model.mongo_model import MongoModel

# from spaceone.inventory_v2.model.reference_resource_model import ReferenceResource
from spaceone.inventory_v2.model.asset_type.database import AssetType

from spaceone.inventory_v2.error.asset import ERROR_RESOURCE_ALREADY_DELETED
from spaceone.inventory_v2.model.region.region_model import Region


class CollectionInfo(EmbeddedDocument):
    service_account_id = StringField(max_length=40)
    secret_id = StringField(max_length=40)
    collector_id = StringField(max_length=40)
    last_collected_at = DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(self.to_mongo())


class Asset(MongoModel):
    asset_id = StringField(max_length=40, generate_id="asset", unique=True)
    name = StringField(default=None, null=True)
    state = StringField(max_length=20, choices=("ACTIVE", "DISCONNECTED", "DELETED"))
    resource_id = StringField(max_length=255, default=None, null=True)
    ip_addresses = ListField(StringField(max_length=255), default=[])
    external_link = StringField(max_length=255, default=None, null=True)
    data = DictField()
    tags = DictField()
    provider = StringField(max_length=255, default=None, null=True)
    account = StringField(max_length=255, default=None, null=True)
    region_id = StringField(max_length=40, default=None, null=True)
    asset_type_id = StringField(max_length=40)
    collector_id = StringField(max_length=40, default=None, null=True)
    project_id = StringField(max_length=40)
    workspace_id = StringField(max_length=40)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    last_collected_at = DateTimeField(null=True)
    deleted_at = DateTimeField(default=None, null=True)

    meta = {
        "updatable_fields": [
            "name",
            "data",
            "state",
            "account",
            "ip_addresses",
            "external_link",
            "tags",
            "region_id",
            "collector_id",
            "project_id",
            "updated_at",
            "last_collected_at",
            "deleted_at",
        ],
        "minimal_fields": [
            "asset_id",
            "name",
            "asset_type_id",
            "provider",
            "region_id",
            "project_id",
        ],
        "change_query_keys": {
            "user_projects": "project_id",
            "ip_address": "ip_addresses",
        },
        "reference_query_keys": {
            "ref_asset_type_id": {
                "model": AssetType,
                "foreign_key": "ref_asset_type_id",
            },
            "ref_region_id": {"model": Region, "foreign_key": "ref_region_id"},
        },
        "indexes": [
            {
                "fields": ["domain_id", "workspace_id", "state"],
                "name": "COMPOUND_INDEX_FOR_GC_1",
            },
            {
                "fields": ["domain_id", "state", "updated_at"],
                "name": "COMPOUND_INDEX_FOR_GC_2",
            },
            {
                "fields": ["domain_id", "state", "-deleted_at"],
                "name": "COMPOUND_INDEX_FOR_GC_3",
            },
            {
                "fields": [
                    "domain_id",
                    "workspace_id",
                    "state",
                    "resource_id",
                    "provider",
                    "asset_type_id",
                    "asset_id",
                    "account",
                ],
                "name": "COMPOUND_INDEX_FOR_COLLECTOR",
            },
            {
                "fields": [
                    "domain_id",
                    "workspace_id",
                    "state",
                    "provider",
                    "asset_type_id",
                    "project_id",
                    "region_id",
                ],
                "name": "COMPOUND_INDEX_FOR_SEARCH_1",
            },
            {
                "fields": [
                    "domain_id",
                    "workspace_id",
                    "state",
                    "asset_type_id",
                    "project_id",
                    "region_id",
                ],
                "name": "COMPOUND_INDEX_FOR_SEARCH_2",
            },
            {
                "fields": [
                    "domain_id",
                    "workspace_id",
                    "state",
                    "-created_at",
                    "project_id",
                ],
                "name": "COMPOUND_INDEX_FOR_SEARCH_3",
            },
            {
                "fields": [
                    "domain_id",
                    "workspace_id",
                    "state",
                    "-deleted_at",
                    "project_id",
                ],
                "name": "COMPOUND_INDEX_FOR_SEARCH_4",
            },
            "resource_id",
            "state",
            "workspace_id",
            "domain_id",
        ],
    }

    def update(self, data):
        if self.state == "DELETED":
            raise ERROR_RESOURCE_ALREADY_DELETED(
                resource_type="Asset", resource_id=self.asset_id
            )

        return super().update(data)

    def delete(self):
        if self.state == "DELETED":
            raise ERROR_RESOURCE_ALREADY_DELETED(
                resource_type="Asset", resource_id=self.asset_id
            )

        self.update({"state": "DELETED", "deleted_at": datetime.utcnow()})
