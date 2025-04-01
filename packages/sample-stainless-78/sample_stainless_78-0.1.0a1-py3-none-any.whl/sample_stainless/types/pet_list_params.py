# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["PetListParams"]


class PetListParams(TypedDict, total=False):
    limit: int
    """maximum number of results to return"""

    tags: List[str]
    """tags to filter by"""
