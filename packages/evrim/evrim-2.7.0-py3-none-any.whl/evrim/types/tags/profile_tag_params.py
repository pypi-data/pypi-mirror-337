# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["ProfileTagParams"]


class ProfileTagParams(TypedDict, total=False):
    profile_ids: Required[Iterable[int]]
