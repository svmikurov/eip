"""Product domain."""

from dataclasses import dataclass


@dataclass
class Product:
    """Product."""

    brand_id: int
    brand_name: str
