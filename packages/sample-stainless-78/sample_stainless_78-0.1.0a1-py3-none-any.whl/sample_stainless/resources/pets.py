# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import pet_add_params, pet_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
from ..types.pet import Pet
from .._base_client import make_request_options
from ..types.pet_list_response import PetListResponse

__all__ = ["PetsResource", "AsyncPetsResource"]


class PetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/seiyeah78/stainless-sample-python#accessing-raw-response-data-eg-headers
        """
        return PetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/seiyeah78/stainless-sample-python#with_streaming_response
        """
        return PetsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """
        Returns a user based on a single ID, if the user does not have access to the pet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/pets/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PetListResponse:
        """
        Returns all pets from the system that the user has access to Nam sed condimentum
        est. Maecenas tempor sagittis sapien, nec rhoncus sem sagittis sit amet. Aenean
        at gravida augue, ac iaculis sem. Curabitur odio lorem, ornare eget elementum
        nec, cursus id lectus. Duis mi turpis, pulvinar ac eros ac, tincidunt varius
        justo. In hac habitasse platea dictumst. Integer at adipiscing ante, a sagittis
        ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus id aliquam diam.
        Cras quis velit non tortor eleifend sagittis. Praesent at enim pharetra urna
        volutpat venenatis eget eget mauris. In eleifend fermentum facilisis. Praesent
        enim enim, gravida ac sodales sed, placerat id erat. Suspendisse lacus dolor,
        consectetur non augue vel, vehicula interdum libero. Morbi euismod sagittis
        libero sed lacinia.

        Sed tempus felis lobortis leo pulvinar rutrum. Nam mattis velit nisl, eu
        condimentum ligula luctus nec. Phasellus semper velit eget aliquet faucibus. In
        a mattis elit. Phasellus vel urna viverra, condimentum lorem id, rhoncus nibh.
        Ut pellentesque posuere elementum. Sed a varius odio. Morbi rhoncus ligula
        libero, vel eleifend nunc tristique vitae. Fusce et sem dui. Aenean nec
        scelerisque tortor. Fusce malesuada accumsan magna vel tempus. Quisque mollis
        felis eu dolor tristique, sit amet auctor felis gravida. Sed libero lorem,
        molestie sed nisl in, accumsan tempor nisi. Fusce sollicitudin massa ut lacinia
        mattis. Sed vel eleifend lorem. Pellentesque vitae felis pretium, pulvinar elit
        eu, euismod sapien.

        Args:
          limit: maximum number of results to return

          tags: tags to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "tags": tags,
                    },
                    pet_list_params.PetListParams,
                ),
            ),
            cast_to=PetListResponse,
        )

    def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        deletes a single pet based on the ID supplied

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/pets/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def add(
        self,
        *,
        name: str,
        tag: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """Creates a new pet in the store.

        Duplicates are allowed

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/pets",
            body=maybe_transform(
                {
                    "name": name,
                    "tag": tag,
                },
                pet_add_params.PetAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )


class AsyncPetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/seiyeah78/stainless-sample-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/seiyeah78/stainless-sample-python#with_streaming_response
        """
        return AsyncPetsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """
        Returns a user based on a single ID, if the user does not have access to the pet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/pets/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PetListResponse:
        """
        Returns all pets from the system that the user has access to Nam sed condimentum
        est. Maecenas tempor sagittis sapien, nec rhoncus sem sagittis sit amet. Aenean
        at gravida augue, ac iaculis sem. Curabitur odio lorem, ornare eget elementum
        nec, cursus id lectus. Duis mi turpis, pulvinar ac eros ac, tincidunt varius
        justo. In hac habitasse platea dictumst. Integer at adipiscing ante, a sagittis
        ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus id aliquam diam.
        Cras quis velit non tortor eleifend sagittis. Praesent at enim pharetra urna
        volutpat venenatis eget eget mauris. In eleifend fermentum facilisis. Praesent
        enim enim, gravida ac sodales sed, placerat id erat. Suspendisse lacus dolor,
        consectetur non augue vel, vehicula interdum libero. Morbi euismod sagittis
        libero sed lacinia.

        Sed tempus felis lobortis leo pulvinar rutrum. Nam mattis velit nisl, eu
        condimentum ligula luctus nec. Phasellus semper velit eget aliquet faucibus. In
        a mattis elit. Phasellus vel urna viverra, condimentum lorem id, rhoncus nibh.
        Ut pellentesque posuere elementum. Sed a varius odio. Morbi rhoncus ligula
        libero, vel eleifend nunc tristique vitae. Fusce et sem dui. Aenean nec
        scelerisque tortor. Fusce malesuada accumsan magna vel tempus. Quisque mollis
        felis eu dolor tristique, sit amet auctor felis gravida. Sed libero lorem,
        molestie sed nisl in, accumsan tempor nisi. Fusce sollicitudin massa ut lacinia
        mattis. Sed vel eleifend lorem. Pellentesque vitae felis pretium, pulvinar elit
        eu, euismod sapien.

        Args:
          limit: maximum number of results to return

          tags: tags to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "tags": tags,
                    },
                    pet_list_params.PetListParams,
                ),
            ),
            cast_to=PetListResponse,
        )

    async def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        deletes a single pet based on the ID supplied

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/pets/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def add(
        self,
        *,
        name: str,
        tag: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """Creates a new pet in the store.

        Duplicates are allowed

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/pets",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "tag": tag,
                },
                pet_add_params.PetAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )


class PetsResourceWithRawResponse:
    def __init__(self, pets: PetsResource) -> None:
        self._pets = pets

        self.retrieve = to_raw_response_wrapper(
            pets.retrieve,
        )
        self.list = to_raw_response_wrapper(
            pets.list,
        )
        self.delete = to_raw_response_wrapper(
            pets.delete,
        )
        self.add = to_raw_response_wrapper(
            pets.add,
        )


class AsyncPetsResourceWithRawResponse:
    def __init__(self, pets: AsyncPetsResource) -> None:
        self._pets = pets

        self.retrieve = async_to_raw_response_wrapper(
            pets.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            pets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            pets.delete,
        )
        self.add = async_to_raw_response_wrapper(
            pets.add,
        )


class PetsResourceWithStreamingResponse:
    def __init__(self, pets: PetsResource) -> None:
        self._pets = pets

        self.retrieve = to_streamed_response_wrapper(
            pets.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            pets.list,
        )
        self.delete = to_streamed_response_wrapper(
            pets.delete,
        )
        self.add = to_streamed_response_wrapper(
            pets.add,
        )


class AsyncPetsResourceWithStreamingResponse:
    def __init__(self, pets: AsyncPetsResource) -> None:
        self._pets = pets

        self.retrieve = async_to_streamed_response_wrapper(
            pets.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            pets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            pets.delete,
        )
        self.add = async_to_streamed_response_wrapper(
            pets.add,
        )
