from rest_framework.pagination import PageNumberPagination


class MaterialsPaginator(PageNumberPagination):
    page_size = 10  # Количество материалов на странице
    max_page_size = 100
