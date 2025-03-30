from __future__ import annotations
from pydantic import Field, model_validator
from typing import Dict, Any
from typing_extensions import Self
from .general import BaseGeneralParameters

class BaseClientParameters:
    class Get(
        BaseGeneralParameters.Search,
        BaseGeneralParameters.Pagination,
        BaseGeneralParameters.Check
    ):
        sort_columns:list[BaseGeneralParameters.SortColumn] = Field([BaseGeneralParameters.SortColumn(name="id", order=BaseGeneralParameters.SortOrder.ASC)], description="List of columns to be sorted")
        date_filters:list[BaseGeneralParameters.DateFilter] = Field([], description="Date filters to be applied")

    class GetQuery(
        BaseGeneralParameters.Filters,
        BaseGeneralParameters.Sorts,
        Get
    ):

        @model_validator(mode="after")
        def set_sort(self) -> Self:
            #* Process sort_columns parameters
            sort = []
            for item in self.sort_columns:
                sort.append(f"{item.name}.{item.order.value}")

            #* Only update if we have valid sort, otherwise keep the default
            if sort:
                self.sort = sort

            return self

        @model_validator(mode="after")
        def set_filter(self) -> Self:
            #* Process filter parameters
            filter = []
            for item in self.date_filters:
                if item.from_date or item.to_date:
                    filter_string = item.name
                    if item.from_date:
                        filter_string += f"|from::{item.from_date.isoformat()}"
                    if item.to_date:
                        filter_string += f"|to::{item.to_date.isoformat()}"
                    filter.append(filter_string)

            #* Only update if we have valid filter, otherwise keep the default
            if filter:
                self.filter = filter

            return self
            
        def to_query_params(self) -> Dict[str, Any]:
            params = {
                "page": self.page,
                "limit": self.limit,
                "search": self.search,
                "sort": self.sort,
                "filter": self.filter,
            }
            if hasattr(self, "is_deleted") and self.is_deleted is not None:
                params["is_deleted"] = self.is_deleted
            if hasattr(self, "is_active") and self.is_active is not None:
                params["is_active"] = self.is_active
            return params