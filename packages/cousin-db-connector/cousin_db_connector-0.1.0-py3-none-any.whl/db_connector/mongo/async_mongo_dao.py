from math import ceil
from fastapi import status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..base_dao import BaseDAO
from ..exceptions import HttpException


class AsyncMongoDAO(BaseDAO):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, tenant_id: str = None):
        """
        DAO for MongoDB with async support.

        :param db: Connection to the database.
        :param collection_name: Name of the collection in the database.
        :param tenant_id: ID del tenant para lógica multi-tenant.
        """
        super().__init__(db, collection_name, tenant_id)

    async def insert(self, data: dict) -> str:
        """Insert a new document in MongoDB with tenant_id filter if necessary."""
        try:
            data = self._apply_tenant_filter(data)
            result = await self._db[self._collection_name].insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_all(self):
        """Get all documents in MongoDB with filter by tenant_id if applicable."""
        try:
            query = self._apply_tenant_filter({})
            cursor = self._db[self._collection_name].find(query)
            return await cursor.to_list(length=None)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_by_id(self, item_id: str):
        """Search for a document by ID in MongoDB, ensuring filtering by tenant_id."""
        try:
            query = self._apply_tenant_filter({"_id": ObjectId(item_id)})
            document = await self._db[self._collection_name].find_one(query)
            return document if document else None
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_paginated(self, filter_query: dict, page: int = 1, page_size: int = 10) -> dict:
        """
        Retrieves paginated documents from the collection with an optional filter.

        :param filter_query: Dictionary with search filters.
        :param page: Number of the page to retrieve (by default 1).
        :param page_size: Number of items per page (by default 10).
        :return: Dictionary with the results and pagination information.
        """
        try:
            query = self._apply_tenant_filter(filter_query)

            total_items = await self._db[self._collection_name].count_documents(query)
            total_pages = ceil(total_items / page_size)
            skip = (page - 1) * page_size

            cursor = (
                self._db[self._collection_name]
                .find(query)
                .skip(skip)
                .limit(page_size)
            )

            items = await cursor.to_list(length=page_size)

            return {
                "results": items,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "page_size": page_size,
                    "total_results": total_items,
                }
            }
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def update(self, item_id: str, update_data: dict) -> bool:
        """Updates a document in MongoDB with filter by tenant_id if applicable."""
        try:
            query = self._apply_tenant_filter({"_id": ObjectId(item_id)})
            result = await self._db[self._collection_name].update_one(query, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def delete(self, item_id: str) -> bool:
        """Delete a document in MongoDB, ensuring filtering by tenant_id."""
        try:
            query = self._apply_tenant_filter({"_id": ObjectId(item_id)})
            result = await self._db[self._collection_name].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))