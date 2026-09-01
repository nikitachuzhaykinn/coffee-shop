from django.http import HttpResponse

def category_detail(request, slug):
    return HttpResponse(f"Страница категории: {slug} (дизайн будет добавлен позже)")

def product_detail(request, slug):
    return HttpResponse(f"Страница товара: {slug} (дизайн будет добавлен позже)")