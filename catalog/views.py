from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Поиск
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            
        # Фильтрация по категории (для общего списка)
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        sort_mapping = {
            'price_asc': 'price',
            'price_desc': '-price',
            'name': 'name',
            'date_desc': '-created_at',
        }
        order_by = sort_mapping.get(sort, '-created_at')
        queryset = queryset.order_by(order_by)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = None
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'date_desc')
        return context


class CategoryDetailView(ProductListView):
    template_name = 'catalog/category_detail.html'

    def get_queryset(self):
        # Получаем queryset с поиском и сортировкой от родителя
        queryset = super().get_queryset()
        # Принудительно фильтруем по категории из URL
        return queryset.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['current_category'] = context['category']
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    queryset = Product.objects.filter(is_active=True).prefetch_related('modifiers__options')