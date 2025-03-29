# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import external_document_processing_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.external_document_processing_list_response import ExternalDocumentProcessingListResponse
from ..types.external_document_processing_create_response import ExternalDocumentProcessingCreateResponse
from ..types.external_document_processing_retrieve_response import ExternalDocumentProcessingRetrieveResponse

__all__ = ["ExternalDocumentProcessingResource", "AsyncExternalDocumentProcessingResource"]


class ExternalDocumentProcessingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExternalDocumentProcessingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/VeritasLabsInc/veritas-api-python#accessing-raw-response-data-eg-headers
        """
        return ExternalDocumentProcessingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExternalDocumentProcessingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/VeritasLabsInc/veritas-api-python#with_streaming_response
        """
        return ExternalDocumentProcessingResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        external_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingCreateResponse:
        """
        Creates a external document processing

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/external_document_processing",
            body=maybe_transform(
                {"external_id": external_id},
                external_document_processing_create_params.ExternalDocumentProcessingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingRetrieveResponse:
        """
        Get external document processing status and results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/external_document_processing/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingRetrieveResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingListResponse:
        """Returns all existing external document processing"""
        return self._get(
            "/v1/external_document_processing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingListResponse,
        )


class AsyncExternalDocumentProcessingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExternalDocumentProcessingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/VeritasLabsInc/veritas-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExternalDocumentProcessingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExternalDocumentProcessingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/VeritasLabsInc/veritas-api-python#with_streaming_response
        """
        return AsyncExternalDocumentProcessingResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        external_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingCreateResponse:
        """
        Creates a external document processing

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/external_document_processing",
            body=await async_maybe_transform(
                {"external_id": external_id},
                external_document_processing_create_params.ExternalDocumentProcessingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingRetrieveResponse:
        """
        Get external document processing status and results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/external_document_processing/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingRetrieveResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExternalDocumentProcessingListResponse:
        """Returns all existing external document processing"""
        return await self._get(
            "/v1/external_document_processing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalDocumentProcessingListResponse,
        )


class ExternalDocumentProcessingResourceWithRawResponse:
    def __init__(self, external_document_processing: ExternalDocumentProcessingResource) -> None:
        self._external_document_processing = external_document_processing

        self.create = to_raw_response_wrapper(
            external_document_processing.create,
        )
        self.retrieve = to_raw_response_wrapper(
            external_document_processing.retrieve,
        )
        self.list = to_raw_response_wrapper(
            external_document_processing.list,
        )


class AsyncExternalDocumentProcessingResourceWithRawResponse:
    def __init__(self, external_document_processing: AsyncExternalDocumentProcessingResource) -> None:
        self._external_document_processing = external_document_processing

        self.create = async_to_raw_response_wrapper(
            external_document_processing.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            external_document_processing.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            external_document_processing.list,
        )


class ExternalDocumentProcessingResourceWithStreamingResponse:
    def __init__(self, external_document_processing: ExternalDocumentProcessingResource) -> None:
        self._external_document_processing = external_document_processing

        self.create = to_streamed_response_wrapper(
            external_document_processing.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            external_document_processing.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            external_document_processing.list,
        )


class AsyncExternalDocumentProcessingResourceWithStreamingResponse:
    def __init__(self, external_document_processing: AsyncExternalDocumentProcessingResource) -> None:
        self._external_document_processing = external_document_processing

        self.create = async_to_streamed_response_wrapper(
            external_document_processing.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            external_document_processing.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            external_document_processing.list,
        )
