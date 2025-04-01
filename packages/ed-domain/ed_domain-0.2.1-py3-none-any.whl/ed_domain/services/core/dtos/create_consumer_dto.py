from typing import TypedDict

from ed_domain.services.core.dtos.create_location_dto import \
    CreateLocationDto


class CreateConsumerDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
