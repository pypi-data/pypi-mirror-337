from dataclasses import dataclass
from typing import List, Optional

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.enums.common import ProcessingStatus
from documente_shared.domain.repositories.processing_case import ProcessingCaseRepository
from documente_shared.infrastructure.documente_client import DocumenteClientMixin


@dataclass
class HttpProcessingCaseRepository(
    DocumenteClientMixin,
    ProcessingCaseRepository,
):
    def find(self, case_id: str) -> Optional[ProcessingCase]:
        response = self.session.get(f"{self.base_url}/processing-cases/{case_id}/")
        if response.status_code == 200:
            return ProcessingCase.from_dict(response.json())
        return None

    def persist(self, instance: ProcessingCase) -> ProcessingCase:
        response = self.session.put(
            url=f"{self.base_url}/processing-cases/{instance.uuid}/",
            json=instance.to_dict,
        )
        if response.status_code in [200, 201]:
            return ProcessingCase.from_dict(response.json())
        return instance

    def remove(self, instance: ProcessingCase):
        self.session.delete(f"{self.base_url}/processing-cases/{instance.uuid}/")

    def filter(self, statuses: List[ProcessingStatus]) -> List[ProcessingCase]:
        response = self.session.get(f"{self.base_url}/processing-cases/")
        if response.status_code == 200:
            raw_response = response.json()
            return [
                ProcessingCase.from_dict(item)
                for item in raw_response.get('data', [])
            ]
        return []