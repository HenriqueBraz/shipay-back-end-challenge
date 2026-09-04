from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    state: str
    city: str
    street: str