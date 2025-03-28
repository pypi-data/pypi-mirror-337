# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from evrim.types import (
    CreatedField,
    CreatedFieldListResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCreatedFields:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        created_field = client.created_fields.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Evrim) -> None:
        created_field = client.created_fields.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
            directed_source="directed_source",
            enum_many=True,
            enum_values=["string"],
            keyword_search=True,
            raw_documents=True,
            rel_template={
                "fields": [
                    {
                        "description": "description",
                        "name": "name",
                        "type": "xxx",
                        "id": 0,
                        "directed": True,
                        "enum_many": True,
                        "enum_values": ["string"],
                        "keyword_search": True,
                        "raw_documents": True,
                        "rel_template_id": 0,
                        "sources": ["string"],
                    }
                ],
                "name": "name",
                "description": "description",
                "questions": ["string"],
            },
            source_entity_type="source_entity_type",
            sources=["string"],
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Evrim) -> None:
        created_field = client.created_fields.retrieve(
            0,
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Evrim) -> None:
        created_field = client.created_fields.update(
            id=0,
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Evrim) -> None:
        created_field = client.created_fields.update(
            id=0,
            description="description",
            directed_source="directed_source",
            enum_many=True,
            enum_values=["string"],
            keyword_search=True,
            name="name",
            raw_documents=True,
            rel_template={
                "fields": [
                    {
                        "description": "description",
                        "name": "name",
                        "type": "xxx",
                        "id": 0,
                        "directed": True,
                        "enum_many": True,
                        "enum_values": ["string"],
                        "keyword_search": True,
                        "raw_documents": True,
                        "rel_template_id": 0,
                        "sources": ["string"],
                    }
                ],
                "name": "name",
                "description": "description",
                "questions": ["string"],
            },
            source_entity_type="source_entity_type",
            sources=["string"],
            specification="specification",
            type="xxx",
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Evrim) -> None:
        created_field = client.created_fields.list()
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Evrim) -> None:
        created_field = client.created_fields.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Evrim) -> None:
        created_field = client.created_fields.delete(
            0,
        )
        assert created_field is None

    @parametrize
    def test_raw_response_delete(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert created_field is None

    @parametrize
    def test_streaming_response_delete(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert created_field is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_profile(self, client: Evrim) -> None:
        created_field = client.created_fields.profile(
            field_id="321669910225",
            profile_id=0,
        )
        assert created_field is None

    @parametrize
    def test_raw_response_profile(self, client: Evrim) -> None:
        response = client.created_fields.with_raw_response.profile(
            field_id="321669910225",
            profile_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert created_field is None

    @parametrize
    def test_streaming_response_profile(self, client: Evrim) -> None:
        with client.created_fields.with_streaming_response.profile(
            field_id="321669910225",
            profile_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert created_field is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_profile(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `field_id` but received ''"):
            client.created_fields.with_raw_response.profile(
                field_id="",
                profile_id=0,
            )


class TestAsyncCreatedFields:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
            directed_source="directed_source",
            enum_many=True,
            enum_values=["string"],
            keyword_search=True,
            raw_documents=True,
            rel_template={
                "fields": [
                    {
                        "description": "description",
                        "name": "name",
                        "type": "xxx",
                        "id": 0,
                        "directed": True,
                        "enum_many": True,
                        "enum_values": ["string"],
                        "keyword_search": True,
                        "raw_documents": True,
                        "rel_template_id": 0,
                        "sources": ["string"],
                    }
                ],
                "name": "name",
                "description": "description",
                "questions": ["string"],
            },
            source_entity_type="source_entity_type",
            sources=["string"],
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.create(
            description="description",
            name="name",
            specification="specification",
            type="xxx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.retrieve(
            0,
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.update(
            id=0,
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.update(
            id=0,
            description="description",
            directed_source="directed_source",
            enum_many=True,
            enum_values=["string"],
            keyword_search=True,
            name="name",
            raw_documents=True,
            rel_template={
                "fields": [
                    {
                        "description": "description",
                        "name": "name",
                        "type": "xxx",
                        "id": 0,
                        "directed": True,
                        "enum_many": True,
                        "enum_values": ["string"],
                        "keyword_search": True,
                        "raw_documents": True,
                        "rel_template_id": 0,
                        "sources": ["string"],
                    }
                ],
                "name": "name",
                "description": "description",
                "questions": ["string"],
            },
            source_entity_type="source_entity_type",
            sources=["string"],
            specification="specification",
            type="xxx",
        )
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert_matches_type(CreatedField, created_field, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert_matches_type(CreatedField, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.list()
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert_matches_type(CreatedFieldListResponse, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.delete(
            0,
        )
        assert created_field is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert created_field is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert created_field is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_profile(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.created_fields.profile(
            field_id="321669910225",
            profile_id=0,
        )
        assert created_field is None

    @parametrize
    async def test_raw_response_profile(self, async_client: AsyncEvrim) -> None:
        response = await async_client.created_fields.with_raw_response.profile(
            field_id="321669910225",
            profile_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert created_field is None

    @parametrize
    async def test_streaming_response_profile(self, async_client: AsyncEvrim) -> None:
        async with async_client.created_fields.with_streaming_response.profile(
            field_id="321669910225",
            profile_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert created_field is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_profile(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `field_id` but received ''"):
            await async_client.created_fields.with_raw_response.profile(
                field_id="",
                profile_id=0,
            )
