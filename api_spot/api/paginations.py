from rest_framework.pagination import PageNumberPagination


class SixPageNumberPagination(PageNumberPagination):
    page_size = 6
