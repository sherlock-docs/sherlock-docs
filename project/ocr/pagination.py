from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page_number, previous_page_number = (None, None)
        if self.page.has_next():
            next_page_number = self.page.next_page_number()
        if self.page.has_previous():
            previous_page_number = self.page.previous_page_number()
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', next_page_number),
            ('previous', previous_page_number),
            ('page_size', self.page.paginator.per_page),
            ('results', data)
        ]))
