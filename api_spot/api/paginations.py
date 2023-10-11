from rest_framework.pagination import PageNumberPagination


class FourPageNumberPagination(PageNumberPagination):
    page_size = 4
