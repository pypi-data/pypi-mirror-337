# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "ExternalDocumentProcessingRetrieveResponse",
    "Candidate",
    "CandidateEducationHistory",
    "CandidateLocation",
    "CandidateWorkHistory",
    "Document",
    "DocumentProcessedAttributes",
    "DocumentProcessedAttributesAttribute",
    "DocumentProcessedAttributesEducationHistory",
    "DocumentProcessedAttributesLocation",
    "DocumentProcessedAttributesWorkHistory",
]


class CandidateEducationHistory(BaseModel):
    degree: Optional[str] = None

    end_date: Optional[str] = None

    name: Optional[str] = None
    """Name of the school including location"""

    start_date: Optional[str] = None


class CandidateLocation(BaseModel):
    value: str
    """Name of the location"""

    category: Optional[str] = None

    details: Optional[str] = None


class CandidateWorkHistory(BaseModel):
    end_date: Optional[str] = None

    name: Optional[str] = None
    """Name of the company including location"""

    role: Optional[str] = None

    start_date: Optional[str] = None


class Candidate(BaseModel):
    clinical_role: Optional[Literal["rn", "lpn", "cna", "allied_health", "other"]] = None

    education_history: Optional[List[CandidateEducationHistory]] = None

    email: Optional[str] = None

    location: Optional[List[CandidateLocation]] = None

    name: Optional[str] = None

    phone: Optional[str] = None

    specialty: Optional[str] = None

    work_history: Optional[List[CandidateWorkHistory]] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> str: ...


class DocumentProcessedAttributesAttribute(BaseModel):
    key: Optional[str] = None

    value: Optional[str] = None


class DocumentProcessedAttributesEducationHistory(BaseModel):
    degree: Optional[str] = None

    end_date: Optional[str] = None

    name: Optional[str] = None
    """Name of the school including location"""

    start_date: Optional[str] = None


class DocumentProcessedAttributesLocation(BaseModel):
    value: str
    """Name of the location"""

    category: Optional[str] = None

    details: Optional[str] = None


class DocumentProcessedAttributesWorkHistory(BaseModel):
    end_date: Optional[str] = None

    name: Optional[str] = None
    """Name of the company including location"""

    role: Optional[str] = None

    start_date: Optional[str] = None


class DocumentProcessedAttributes(BaseModel):
    attributes: Optional[List[DocumentProcessedAttributesAttribute]] = None

    education_history: Optional[List[DocumentProcessedAttributesEducationHistory]] = None

    locations: Optional[List[DocumentProcessedAttributesLocation]] = None

    work_history: Optional[List[DocumentProcessedAttributesWorkHistory]] = None


class Document(BaseModel):
    id: str

    filename: str

    processed_attributes: Optional[DocumentProcessedAttributes] = None


class ExternalDocumentProcessingRetrieveResponse(BaseModel):
    id: str

    status: Literal["pending", "processing", "completed", "failed"]

    candidate: Optional[Candidate] = None

    documents: Optional[List[Document]] = None
