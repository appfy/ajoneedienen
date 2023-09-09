from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from main.models import Banner
from main.models import CartItem
from main.models import CatalogueAd
from main.models import Category
from main.models import CheckoutAd
from main.models import Notification
from main.models import Restaurant
from main.models import ProductAd


class IndexView(ListView):
    model = Restaurant
    template_name = "web/index.html"
    context_object_name = "restaurants"
    paginate_by = 50


class RestaurantCatalogueView(DetailView):
    model = Restaurant
    template_name = "web/catalogue.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        restaurant = self.get_object()
        context = super().get_context_data(**kwargs)
        context["banners"] = Banner.objects.filter(restaurant=self.get_object())
        context["notifications"] = Notification.objects.filter(restaurant=self.get_object())
        context["product_ads"] = ProductAd.objects.filter(
            display_upto__gte=timezone.now(), display_in__in=[restaurant]
        )
        return context


class CategoryView(DetailView):
    model = Category
    template_name = "web/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object().restaurant
        session_key = self.request.session.session_key
        cart_items = CartItem.objects.filter(restaurant=restaurant, session_key=session_key)
        context["cart_items"] = cart_items
        context["total_price"] = sum([cart_item.total_price() for cart_item in cart_items])
        context["restaurant"] = restaurant
        context["banners"] = Banner.objects.filter(restaurant=restaurant)
        context["catalogue_ads"] = CatalogueAd.objects.filter(
            display_upto__gte=timezone.now(), display_in__in=[restaurant]
        )
        context["product_ads"] = ProductAd.objects.filter(
            display_upto__gte=timezone.now(), display_in__in=[restaurant]
        )
        return context


class CheckoutView(DetailView):
    model = Restaurant
    template_name = "web/checkout.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        session_key = self.request.session.session_key
        cart_items = CartItem.objects.filter(restaurant=restaurant, session_key=session_key)
        context["banners"] = Banner.objects.filter(restaurant=restaurant)
        context["restaurant"] = restaurant
        context["cart_items"] = cart_items
        context["total_price"] = sum([cart_item.total_price() for cart_item in cart_items])
        context["checkout_ads"] = CheckoutAd.objects.filter(
            display_upto__gte=timezone.now(), display_in__in=[restaurant]
        )
        context["product_ads"] = ProductAd.objects.filter(
            display_upto__gte=timezone.now(), display_in__in=[restaurant]
        )
        return context


class CartItemPlusView(View):
    def get(self, request):
        option_pk = request.GET.get("option")
        restaurant_pk = request.GET.get("restaurant_pk")
        session_key = request.GET.get("session_key")
        cart_item = CartItem.objects.get_or_create(
            product_id=option_pk, restaurant_id=restaurant_pk, session_key=session_key
        )[0]
        cart_item.quantity += 1
        cart_item.save()
        response = {"success": True, "quantity": cart_item.quantity, "subtotal": cart_item.total_price()}
        return JsonResponse(response)


class CartItemMinusView(View):
    def get(self, request):
        option_pk = request.GET.get("option")
        restaurant_pk = request.GET.get("restaurant_pk")
        session_key = request.GET.get("session_key")
        cart_item = CartItem.objects.get_or_create(
            product_id=option_pk, restaurant_id=restaurant_pk, session_key=session_key
        )[0]
        print(cart_item.quantity, "*" * 20)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            response = {"success": True, "quantity": cart_item.quantity, "subtotal": cart_item.total_price()}
        else:
            cart_item.delete()
            response = {"success": True, "quantity": 0, "subtotal": 0}
        return JsonResponse(response)
