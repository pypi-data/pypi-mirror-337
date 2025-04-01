# Pets

Types:

```python
from sample_stainless.types import NewPet, Pet, PetListResponse
```

Methods:

- <code title="get /pets/{id}">client.pets.<a href="./src/sample_stainless/resources/pets.py">retrieve</a>(id) -> <a href="./src/sample_stainless/types/pet.py">Pet</a></code>
- <code title="get /pets">client.pets.<a href="./src/sample_stainless/resources/pets.py">list</a>(\*\*<a href="src/sample_stainless/types/pet_list_params.py">params</a>) -> <a href="./src/sample_stainless/types/pet_list_response.py">PetListResponse</a></code>
- <code title="delete /pets/{id}">client.pets.<a href="./src/sample_stainless/resources/pets.py">delete</a>(id) -> None</code>
- <code title="post /pets">client.pets.<a href="./src/sample_stainless/resources/pets.py">add</a>(\*\*<a href="src/sample_stainless/types/pet_add_params.py">params</a>) -> <a href="./src/sample_stainless/types/pet.py">Pet</a></code>
