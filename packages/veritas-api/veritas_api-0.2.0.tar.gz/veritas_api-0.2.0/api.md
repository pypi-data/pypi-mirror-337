# Enrichments

Types:

```python
from veritas_api.types import EnrichmentRetrieveResponse, EnrichmentCreateBulkResponse
```

Methods:

- <code title="get /v1/enrichments/{id}">client.enrichments.<a href="./src/veritas_api/resources/enrichments.py">retrieve</a>(id) -> <a href="./src/veritas_api/types/enrichment_retrieve_response.py">EnrichmentRetrieveResponse</a></code>
- <code title="post /v1/enrichments">client.enrichments.<a href="./src/veritas_api/resources/enrichments.py">create_bulk</a>(\*\*<a href="src/veritas_api/types/enrichment_create_bulk_params.py">params</a>) -> <a href="./src/veritas_api/types/enrichment_create_bulk_response.py">EnrichmentCreateBulkResponse</a></code>

# ExternalDocumentProcessing

Types:

```python
from veritas_api.types import (
    ExternalDocumentProcessingCreateResponse,
    ExternalDocumentProcessingRetrieveResponse,
    ExternalDocumentProcessingListResponse,
)
```

Methods:

- <code title="post /v1/external_document_processing">client.external_document_processing.<a href="./src/veritas_api/resources/external_document_processing.py">create</a>(\*\*<a href="src/veritas_api/types/external_document_processing_create_params.py">params</a>) -> <a href="./src/veritas_api/types/external_document_processing_create_response.py">ExternalDocumentProcessingCreateResponse</a></code>
- <code title="get /v1/external_document_processing/{id}">client.external_document_processing.<a href="./src/veritas_api/resources/external_document_processing.py">retrieve</a>(id) -> <a href="./src/veritas_api/types/external_document_processing_retrieve_response.py">ExternalDocumentProcessingRetrieveResponse</a></code>
- <code title="get /v1/external_document_processing">client.external_document_processing.<a href="./src/veritas_api/resources/external_document_processing.py">list</a>() -> <a href="./src/veritas_api/types/external_document_processing_list_response.py">ExternalDocumentProcessingListResponse</a></code>
