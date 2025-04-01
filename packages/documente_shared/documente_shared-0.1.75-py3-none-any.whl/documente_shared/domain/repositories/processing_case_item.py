from abc import ABC, abstractmethod
from typing import Optional, List

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.entities.processing_case_item import ProcessingCaseItem
from documente_shared.domain.entities.processing_case_item_filters import ProcessingCaseItemFilters


class ProcessingCaseItemRepository(ABC):

    @abstractmethod
    def find(self, uuid: str) -> Optional[ProcessingCaseItem]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, instance: ProcessingCaseItem) -> ProcessingCaseItem:
        raise NotImplementedError

    @abstractmethod
    def remove(self, instance: ProcessingCaseItem):
        raise NotImplementedError

    @abstractmethod
    def filter(self, tenant_slug: str, filters: ProcessingCaseItemFilters) -> List[ProcessingCase]:
        raise NotImplementedError
