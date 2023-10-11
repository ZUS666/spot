from rest_framework.pagination import PageNumberPagination


class SixPageNumberPagination(PageNumberPagination):
    page_size = 6


class ThreePageNumberPagination(PageNumberPagination):
    page_size = 3


class FourPageNumberPagination(PageNumberPagination):
    page_size = 4
