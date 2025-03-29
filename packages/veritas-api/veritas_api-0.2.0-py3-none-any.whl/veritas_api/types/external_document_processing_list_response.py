# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["ExternalDocumentProcessingListResponse", "ExternalDocumentProcessingListResponseItem"]


class ExternalDocumentProcessingListResponseItem(BaseModel):
    id: str

    status: Literal["pending", "processing", "errored", "completed"]


ExternalDocumentProcessingListResponse: TypeAlias = List[ExternalDocumentProcessingListResponseItem]
