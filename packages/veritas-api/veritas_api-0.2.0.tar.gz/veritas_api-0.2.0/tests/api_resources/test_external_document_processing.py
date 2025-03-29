# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from veritas_api import VeritasAPI, AsyncVeritasAPI
from veritas_api.types import (
    ExternalDocumentProcessingListResponse,
    ExternalDocumentProcessingCreateResponse,
    ExternalDocumentProcessingRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExternalDocumentProcessing:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: VeritasAPI) -> None:
        external_document_processing = client.external_document_processing.create(
            external_id="external_id",
        )
        assert_matches_type(ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: VeritasAPI) -> None:
        response = client.external_document_processing.with_raw_response.create(
            external_id="external_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = response.parse()
        assert_matches_type(ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: VeritasAPI) -> None:
        with client.external_document_processing.with_streaming_response.create(
            external_id="external_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = response.parse()
            assert_matches_type(
                ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: VeritasAPI) -> None:
        external_document_processing = client.external_document_processing.retrieve(
            "id",
        )
        assert_matches_type(ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: VeritasAPI) -> None:
        response = client.external_document_processing.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = response.parse()
        assert_matches_type(ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: VeritasAPI) -> None:
        with client.external_document_processing.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = response.parse()
            assert_matches_type(
                ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: VeritasAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.external_document_processing.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: VeritasAPI) -> None:
        external_document_processing = client.external_document_processing.list()
        assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: VeritasAPI) -> None:
        response = client.external_document_processing.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = response.parse()
        assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: VeritasAPI) -> None:
        with client.external_document_processing.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = response.parse()
            assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncExternalDocumentProcessing:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVeritasAPI) -> None:
        external_document_processing = await async_client.external_document_processing.create(
            external_id="external_id",
        )
        assert_matches_type(ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVeritasAPI) -> None:
        response = await async_client.external_document_processing.with_raw_response.create(
            external_id="external_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = await response.parse()
        assert_matches_type(ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVeritasAPI) -> None:
        async with async_client.external_document_processing.with_streaming_response.create(
            external_id="external_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = await response.parse()
            assert_matches_type(
                ExternalDocumentProcessingCreateResponse, external_document_processing, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVeritasAPI) -> None:
        external_document_processing = await async_client.external_document_processing.retrieve(
            "id",
        )
        assert_matches_type(ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVeritasAPI) -> None:
        response = await async_client.external_document_processing.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = await response.parse()
        assert_matches_type(ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVeritasAPI) -> None:
        async with async_client.external_document_processing.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = await response.parse()
            assert_matches_type(
                ExternalDocumentProcessingRetrieveResponse, external_document_processing, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVeritasAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.external_document_processing.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVeritasAPI) -> None:
        external_document_processing = await async_client.external_document_processing.list()
        assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVeritasAPI) -> None:
        response = await async_client.external_document_processing.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        external_document_processing = await response.parse()
        assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVeritasAPI) -> None:
        async with async_client.external_document_processing.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            external_document_processing = await response.parse()
            assert_matches_type(ExternalDocumentProcessingListResponse, external_document_processing, path=["response"])

        assert cast(Any, response.is_closed) is True
