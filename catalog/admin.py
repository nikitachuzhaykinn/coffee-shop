from django.contrib import admin
from .models import Category, Product, Modifier, ModifierOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    

class ModifierOptionInline(admin.TabularInline):
    model = ModifierOption
    extra = 1
    

class ModifierInline(admin.StackedInline):
    model = Modifier
    extra = 1
    inlines = [ModifierOptionInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'category', 'price', 'description', 'image', 'is_active']
    list_display = ['name', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModifierInline]
    
    
@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']
    
    
@admin.register(ModifierOption)
class ModifierOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'modifier', 'price_extra']
    
    
original_get_app_list = admin.site.__class__.get_app_list

def get_app_list(self, request):
    app_list = original_get_app_list(self, request)
    for app in app_list:
        if app['app_label'] == 'catalog':
            model_order = ['Category', 'Product', 'Modifier', 'ModifierOption']
            app['models'].sort(key=lambda x: model_order.index(x['object_name']) if x['object_name'] in model_order else 99)
    return app_list

admin.site.__class__.get_app_list = get_app_list