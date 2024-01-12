from django.http import HttpResponse


def post_list(request, year: None, month: None):
    if month is not None:
        return HttpResponse(f"post list archive for {year} and {month}")

    if year is not None:
        return HttpResponse(f"post list archive for {year}")
    return HttpResponse("<h1>H1 tag</h1><br><h2>H2 tag</h2>")


def category_list(request):
    return HttpResponse("category list page")


def post_detail(request, post_slug):
    return HttpResponse(f"post detail {post_slug}")


def costom_post_detail(request):
    return HttpResponse(f"costom post detail")


def categories_list():
    return None
