# djangify_backend/apps/core/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from typing import Any, Dict
from urllib import parse


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that provides:
    - Configurable page size
    - Page size query parameter support
    - First and last page URLs
    - Consistent response format
    """

    page_size = 12  # Default page size
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def remove_query_param(self, url: str, key: str) -> str:
        """
        Given a URL and a key, remove that query parameter from the URL.
        """
        parsed = parse.urlparse(url)
        query_dict = dict(parse.parse_qsl(parsed.query))
        query_dict.pop(key, None)
        new_query = parse.urlencode(query_dict)
        return parse.urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

    def replace_query_param(self, url: str, key: str, value: Any) -> str:
        """
        Given a URL and a key/value pair, set or replace that query parameter in the URL.
        """
        parsed = parse.urlparse(url)
        query_dict = dict(parse.parse_qsl(parsed.query))
        query_dict[key] = value
        new_query = parse.urlencode(query_dict)
        return parse.urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

    def get_paginated_response(self, data: Any) -> Response:
        """
        Enhance the pagination response with additional metadata
        """
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("total_pages", self.page.paginator.num_pages),
                    ("current_page", self.page.number),
                    ("page_size", self.get_page_size(self.request)),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("first", self.get_first_link()),
                    ("last", self.get_last_link()),
                    ("results", data),
                ]
            )
        )

    def get_first_link(self) -> str:
        """
        Get URL for the first page
        """
        if not self.page.paginator.num_pages:
            return None
        url = self.request.build_absolute_uri()
        return self.remove_query_param(url, self.page_query_param)

    def get_last_link(self) -> str:
        """
        Get URL for the last page
        """
        if not self.page.paginator.num_pages:
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return self.replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response_schema(self, schema: Dict) -> Dict:
        """
        Override to provide correct OpenAPI schema
        """
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "Total number of items",
                },
                "total_pages": {
                    "type": "integer",
                    "description": "Total number of pages",
                },
                "current_page": {
                    "type": "integer",
                    "description": "Current page number",
                },
                "page_size": {
                    "type": "integer",
                    "description": "Number of items per page",
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "description": "URL for the next page",
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "description": "URL for the previous page",
                },
                "first": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "description": "URL for the first page",
                },
                "last": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "description": "URL for the last page",
                },
                "results": schema,
            },
        }
