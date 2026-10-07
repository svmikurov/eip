"""Product domain."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Product."""

    brand_id: int
    brand_name: str
