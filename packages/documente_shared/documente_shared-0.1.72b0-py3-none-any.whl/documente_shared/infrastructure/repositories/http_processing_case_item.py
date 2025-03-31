from dataclasses import dataclass
from typing import List, Optional

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.entities.processing_case_item import ProcessingCaseItem
from documente_shared.domain.enums.common import ProcessingStatus
from documente_shared.domain.repositories.processing_case_item import ProcessingCaseItemRepository
from documente_shared.infrastructure.documente_client import DocumenteClientMixin


@dataclass
class HttpProcessingCaseItemRepository(
    DocumenteClientMixin,
    ProcessingCaseItemRepository,
):

    def find(self, uuid: str) -> Optional[ProcessingCaseItem]:
        response = self.session.get(f"{self.base_url}/processing-case-items/{uuid}/")
        if response.status_code == 200:
            return ProcessingCaseItem.from_dict(response.json())
        return None

    def persist(self, instance: ProcessingCaseItem) -> ProcessingCaseItem:
        response = self.session.put(
            url=f"{self.base_url}/processing-case-items/{instance.uuid}/",
            json=instance.to_simple_dict,
        )
        if response.status_code in [200, 201]:
            return ProcessingCaseItem.from_dict(response.json())
        return instance

    def remove(self, instance: ProcessingCaseItem):
        self.session.delete(f"{self.base_url}/processing-case-items/{instance.uuid}/")

    def filter(self, statuses: List[ProcessingStatus]) -> List[ProcessingCase]:
        response = self.session.get(f"{self.base_url}/processing-case-items/")
        if response.status_code == 200:
            raw_response = response.json()
            return [
                ProcessingCase.from_dict(item)
                for item in raw_response.get('data', [])
            ]
        return []

    def filter_by_case_id(self, case_id: str) -> List[ProcessingCase]:
        response = self.session.get(f"{self.base_url}/processing-case-items/?case_id={case_id}")
        if response.status_code == 200:
            raw_response = response.json()
            return [
                ProcessingCase.from_dict(item)
                for item in raw_response.get('data', [])
            ]
        return []