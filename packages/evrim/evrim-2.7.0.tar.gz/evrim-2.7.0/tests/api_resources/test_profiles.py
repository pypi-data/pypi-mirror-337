# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from evrim.types import (
    TagProfile,
    ProfileListResponse,
)
from tests.utils import assert_matches_type
from evrim.types.shared import Profile

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        profile = client.profiles.create(
            specification="specification",
            template_id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Evrim) -> None:
        profile = client.profiles.create(
            specification="specification",
            template_id=0,
            source="source",
            source_map={},
            tags=[
                {
                    "name": "name",
                    "description": "description",
                }
            ],
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.create(
            specification="specification",
            template_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.create(
            specification="specification",
            template_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Evrim) -> None:
        profile = client.profiles.retrieve(
            0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Evrim) -> None:
        profile = client.profiles.update(
            id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Evrim) -> None:
        profile = client.profiles.update(
            id=0,
            source="source",
            source_map={},
            specification="specification",
            tags=[
                {
                    "name": "name",
                    "description": "description",
                }
            ],
            template_id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Evrim) -> None:
        profile = client.profiles.list()
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Evrim) -> None:
        profile = client.profiles.list(
            limit=0,
            offset=0,
            specification="specification",
        )
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileListResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Evrim) -> None:
        profile = client.profiles.delete(
            0,
        )
        assert profile is None

    @parametrize
    def test_raw_response_delete(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert profile is None

    @parametrize
    def test_streaming_response_delete(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert profile is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_tag(self, client: Evrim) -> None:
        profile = client.profiles.tag(
            profile_id="321669910225",
            tag_id=0,
        )
        assert_matches_type(TagProfile, profile, path=["response"])

    @parametrize
    def test_raw_response_tag(self, client: Evrim) -> None:
        response = client.profiles.with_raw_response.tag(
            profile_id="321669910225",
            tag_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(TagProfile, profile, path=["response"])

    @parametrize
    def test_streaming_response_tag(self, client: Evrim) -> None:
        with client.profiles.with_streaming_response.tag(
            profile_id="321669910225",
            tag_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(TagProfile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_tag(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            client.profiles.with_raw_response.tag(
                profile_id="",
                tag_id=0,
            )


class TestAsyncProfiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.create(
            specification="specification",
            template_id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.create(
            specification="specification",
            template_id=0,
            source="source",
            source_map={},
            tags=[
                {
                    "name": "name",
                    "description": "description",
                }
            ],
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.create(
            specification="specification",
            template_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.create(
            specification="specification",
            template_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.retrieve(
            0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.update(
            id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.update(
            id=0,
            source="source",
            source_map={},
            specification="specification",
            tags=[
                {
                    "name": "name",
                    "description": "description",
                }
            ],
            template_id=0,
        )
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(Profile, profile, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(Profile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.list()
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.list(
            limit=0,
            offset=0,
            specification="specification",
        )
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileListResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileListResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.delete(
            0,
        )
        assert profile is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert profile is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert profile is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_tag(self, async_client: AsyncEvrim) -> None:
        profile = await async_client.profiles.tag(
            profile_id="321669910225",
            tag_id=0,
        )
        assert_matches_type(TagProfile, profile, path=["response"])

    @parametrize
    async def test_raw_response_tag(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.with_raw_response.tag(
            profile_id="321669910225",
            tag_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(TagProfile, profile, path=["response"])

    @parametrize
    async def test_streaming_response_tag(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.with_streaming_response.tag(
            profile_id="321669910225",
            tag_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(TagProfile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_tag(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            await async_client.profiles.with_raw_response.tag(
                profile_id="",
                tag_id=0,
            )
