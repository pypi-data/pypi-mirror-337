from dataclasses import dataclass
from typing import List, Optional

from documente_shared.domain.entities.documet import DocumentProcessing
from documente_shared.domain.enums.common import ProcessingStatus, DocumentProcessingCategory
from documente_shared.domain.repositories.document_processing import DocumentProcessingRepository
from documente_shared.infrastructure.documente_client import DocumenteClientMixin

class HttpDocumentProcessingRepository(
    DocumenteClientMixin,
    DocumentProcessingRepository,
):
    def find(self, digest: str) -> Optional[DocumentProcessing]:
        response = self.session.get(f"{self.base_url}/documents/{digest}/")
        if response.status_code == 200:
            return DocumentProcessing.from_dict(response.json())
        return None

    def persist(self, instance: DocumentProcessing) -> DocumentProcessing:
        response = self.session.put(
            url=f"{self.base_url}/documents/{instance.uuid}/",
            json=instance.to_simple_dict,
        )
        if response.status_code in [200, 201]:
            return DocumentProcessing.from_dict(response.json())
        return instance
    
    def remove(self, instance: DocumentProcessing):
        self.session.delete(f"{self.base_url}/documents/{instance.uuid}/")
        
    def filter(self, statuses: List[ProcessingStatus]) -> List[DocumentProcessing]:
        response = self.session.get(f"{self.base_url}/processing-cases/{statuses}/")
        if response.status_code == 200:
            raw_response = response.json()
            return [
                DocumentProcessing.from_dict(item)
                for item in raw_response.get('data', [])
            ]
        return []
    
    