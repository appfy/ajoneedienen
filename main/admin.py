from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from import_export.admin import ImportExportActionModelAdmin
from registration.models import RegistrationProfile

from .models import Banner
# from .models import CartItem
from .models import CatalogueAd
from .models import Category
from .models import DefaultCategory
from .models import District
from .models import Notification
from .models import Option
from .models import Product
from .models import ProductAd
from .models import Textiles
from .models import State
from .models import Subcategory


admin.site.unregister(RegistrationProfile)


@admin.register(State)
class StateAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Textiles)
class TextilesAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "user", "phone")
    list_filter = ("name", "user")
    autocomplete_fields = ("user",)
    search_fields = ("name", "user__username")
    readonly_fields = ("created_by",)

    def add_view(self, request, form_url='', extra_context=None):
        self.add_title = "Add Textiles"  # Set the custom heading here
        return super().add_view(request, form_url, extra_context)


@admin.register(DefaultCategory)
class DefaultCategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")
    readonly_fields = ("created_by",)


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "restaurant")
    list_filter = ("restaurant",)
    autocomplete_fields = ("restaurant",)
    search_fields = ("name", "description")
    readonly_fields = ("created_by",)


@admin.register(Subcategory)
class SubcategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    autocomplete_fields = ("category",)
    search_fields = ("name", "description")
    readonly_fields = ("created_by",)


@admin.register(Option)
class OptionAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "product")
    list_filter = ("product",)
    autocomplete_fields = ("product",)
    search_fields = ("name",)
    readonly_fields = ("created_by",)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ("name", "price")


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "subcategory", "description")
    list_filter = ("name", "subcategory")
    autocomplete_fields = ("subcategory",)
    readonly_fields = ("created_by",)
    search_fields = ("name", "description")
    inlines = (OptionInline,)


@admin.register(Banner)
class BannerAdmin(ImportExportActionModelAdmin):
    pass


# @admin.register(CartItem)
# class CartItemAdmin(ImportExportActionModelAdmin):
#     list_display = ("__str__", "restaurant", "quantity", "total_price")
#     list_filter = ("restaurant",)


@admin.register(CatalogueAd)
class CatalogueAdAdmin(ImportExportActionModelAdmin):
    list_display = ("__str__", "display_upto")
    formfield_overrides = {models.ManyToManyField: {'widget': CheckboxSelectMultiple}}

    class Media:
        js = ('custom_admin/script.js',)
        css = {'all': ('custom_admin/style.css',)}


@admin.register(ProductAd)
class ProductAdAdmin(ImportExportActionModelAdmin):
    list_display = ("__str__", "display_upto")
    formfield_overrides = {models.ManyToManyField: {'widget': CheckboxSelectMultiple}}

    class Media:
        js = ('custom_admin/script.js',)
        css = {'all': ('custom_admin/style.css',)}


@admin.register(Notification)
class NotificationAdmin(ImportExportActionModelAdmin):
    list_display = ("restaurant", "notification")
    list_filter = ("restaurant",)
