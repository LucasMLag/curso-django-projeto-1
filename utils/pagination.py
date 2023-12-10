import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = math.floor(qty_pages / 2)
    start_range = current_page - middle_range - 1
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    if start_range < 0:
        start_range_offset = abs(start_range)
        start_range += start_range_offset
        stop_range += start_range_offset

    if stop_range >= total_pages:
        stop_range_offset = stop_range - total_pages
        start_range -= stop_range_offset
        stop_range -= stop_range_offset

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range+1,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, queryset, items_per_page, qty_pages=5):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, items_per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page,
    )

    return page_obj, pagination_range
