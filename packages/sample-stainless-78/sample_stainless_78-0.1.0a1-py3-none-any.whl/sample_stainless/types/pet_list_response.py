# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .pet import Pet

__all__ = ["PetListResponse"]

PetListResponse: TypeAlias = List[Pet]
