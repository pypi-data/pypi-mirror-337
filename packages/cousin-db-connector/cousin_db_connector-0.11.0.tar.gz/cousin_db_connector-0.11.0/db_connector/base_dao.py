from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseDAO(ABC):
    def __init__(self, db, collection_name: str, tenant_id: Optional[str] = None):
        """
        Constructor base for all DAOs.

        :param db: Connection to the database.
        :param collection_name: Name of the collection in the database.
        :param tenant_id: ID del tenant para lógica multi-tenant.
        """
        self._db = db
        self._collection_name = collection_name
        self._tenant_id = tenant_id  #If None, no tenant filter will be applied.

    def _apply_tenant_filter(self, query: dict) -> dict:
        """Apply the tenant filter to the query."""
        if self._tenant_id:
            query["tenant_id"] = self._tenant_id
            query["is_deleted"] = False
        return query

    @abstractmethod
    async def insert(self, data: dict) -> Any:
        """Insert a new document in the database."""
        pass

    @abstractmethod
    async def find_all(self) -> List[dict]:
        """Get all documents from the database."""
        pass

    @abstractmethod
    async def find_by_id(self, item_id: Any) -> dict:
        """Find a document by ID in the database."""
        pass

    @abstractmethod
    async def update(self, item_id: Any, update_data: dict) -> bool:
        """Update a document in the database."""
        pass

    @abstractmethod
    async def delete(self, item_id: Any) -> bool:
        """Delete a document in the database."""
        pass