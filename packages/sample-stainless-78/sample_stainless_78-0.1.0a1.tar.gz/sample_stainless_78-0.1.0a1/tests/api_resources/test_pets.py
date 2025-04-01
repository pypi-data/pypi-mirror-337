# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sample_stainless import SampleStainless, AsyncSampleStainless
from sample_stainless.types import Pet, PetListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SampleStainless) -> None:
        pet = client.pets.retrieve(
            0,
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SampleStainless) -> None:
        response = client.pets.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = response.parse()
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SampleStainless) -> None:
        with client.pets.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = response.parse()
            assert_matches_type(Pet, pet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SampleStainless) -> None:
        pet = client.pets.list()
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SampleStainless) -> None:
        pet = client.pets.list(
            limit=0,
            tags=["string"],
        )
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SampleStainless) -> None:
        response = client.pets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = response.parse()
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SampleStainless) -> None:
        with client.pets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = response.parse()
            assert_matches_type(PetListResponse, pet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: SampleStainless) -> None:
        pet = client.pets.delete(
            0,
        )
        assert pet is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: SampleStainless) -> None:
        response = client.pets.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = response.parse()
        assert pet is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: SampleStainless) -> None:
        with client.pets.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = response.parse()
            assert pet is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_add(self, client: SampleStainless) -> None:
        pet = client.pets.add(
            name="name",
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_add_with_all_params(self, client: SampleStainless) -> None:
        pet = client.pets.add(
            name="name",
            tag="tag",
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_add(self, client: SampleStainless) -> None:
        response = client.pets.with_raw_response.add(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = response.parse()
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_add(self, client: SampleStainless) -> None:
        with client.pets.with_streaming_response.add(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = response.parse()
            assert_matches_type(Pet, pet, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.retrieve(
            0,
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSampleStainless) -> None:
        response = await async_client.pets.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = await response.parse()
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSampleStainless) -> None:
        async with async_client.pets.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = await response.parse()
            assert_matches_type(Pet, pet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.list()
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.list(
            limit=0,
            tags=["string"],
        )
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSampleStainless) -> None:
        response = await async_client.pets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = await response.parse()
        assert_matches_type(PetListResponse, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSampleStainless) -> None:
        async with async_client.pets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = await response.parse()
            assert_matches_type(PetListResponse, pet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.delete(
            0,
        )
        assert pet is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSampleStainless) -> None:
        response = await async_client.pets.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = await response.parse()
        assert pet is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSampleStainless) -> None:
        async with async_client.pets.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = await response.parse()
            assert pet is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_add(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.add(
            name="name",
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncSampleStainless) -> None:
        pet = await async_client.pets.add(
            name="name",
            tag="tag",
        )
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncSampleStainless) -> None:
        response = await async_client.pets.with_raw_response.add(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pet = await response.parse()
        assert_matches_type(Pet, pet, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncSampleStainless) -> None:
        async with async_client.pets.with_streaming_response.add(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pet = await response.parse()
            assert_matches_type(Pet, pet, path=["response"])

        assert cast(Any, response.is_closed) is True
