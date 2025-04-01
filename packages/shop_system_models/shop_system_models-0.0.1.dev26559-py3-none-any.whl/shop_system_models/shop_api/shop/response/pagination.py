from typing import Optional, List, Dict, Any
from pydantic import Field

from shop_system_models.shop_api import MetaBaseModel


class PartialPaginationResponseModel(MetaBaseModel):
    """Base pagination information."""
    total_rows: int
    is_first_page: bool
    is_last_page: bool


class PaginationResponseModel(PartialPaginationResponseModel):
    """Complete pagination information with page and page size."""
    page: int
    page_size: int 