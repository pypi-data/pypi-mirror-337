# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .new_pet import NewPet

__all__ = ["Pet"]


class Pet(NewPet):
    id: int
