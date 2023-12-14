from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Кастомная пагинация. Количество элементов на страницу настраивается при
    помощи параметра limit.
    """
    page_size_query_param = 'limit'
