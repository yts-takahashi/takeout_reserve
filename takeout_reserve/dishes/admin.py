from django.contrib import admin
from .models import Category, Dish, Order, OrderDetail

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderDetailInline,)
    list_display = ('customer', 'ordered_at')

# Register your models here.
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
