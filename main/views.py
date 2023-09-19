from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from registration.views import RegistrationView

from .forms import RestaurantCreateForm
from .forms import RestaurantEditForm
from .mixins import RestaurantRequiredMixin
from .mixins import SuperuserRequiredMixin
from .models import CartItem
from .models import Category
from .models import DefaultCategory
from .models import Notification
from .models import Option
from .models import Product
from .models import Textiles
from .models import Subcategory


class UserRegisterView(RegistrationView):
    success_url = reverse_lazy("main:index")

    def register(self, form):
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
        )
        new_user.is_staff = True
        new_user.save()

        user = authenticate(
            self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1']
        )
        if user is not None:
            login(self.request, user)

        return new_user


class IndexView(LoginRequiredMixin, generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect("main:admin_index")
        elif request.user.is_staff:
            return redirect("main:restaurant_index")
        else:
            return redirect("main:shop_index")


class AdminIndexView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    context_object_name = "products"
    paginate_by = 50
    template_name = "main/admin_index.html"

    def get_queryset(self):
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        context["restaurant_count"] = Textiles.objects.all().count()
        context["product_count"] = Product.objects.all().count()
        context["category_count"] = Category.objects.all().count()
        context["subcategory_count"] = Subcategory.objects.all().count()
        return context


class RestaurantBlockedView(LoginRequiredMixin, generic.TemplateView):
    template_name = "main/restaurant_blocked.html"


class AutoRestaurantUpdateView(LoginRequiredMixin, generic.FormView):
    model = Textiles
    template_name = "main/restaurant_update.html"
    success_url = reverse_lazy("main:index")

    def dispatch(self, request, *args, **kwargs):
        if Textiles.objects.filter(user=self.request.user).exists():
            return redirect("main:admin_index")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if Textiles.objects.filter(user=self.request.user).exists():
            return RestaurantEditForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=Textiles.objects.get(user=self.request.user),
            )
        else:
            return RestaurantEditForm(self.request.POST or None, self.request.FILES or None)

    def form_valid(self, form):
        data = form.save()
        data.user = self.request.user
        data.save()
        for cat in DefaultCategory.objects.all():
            Category.objects.create(restaurant=data, name=cat.name, image=cat.image, description=cat.description)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("data is not saved", form.errors)
        return super().form_invalid(form)


class RestaurantProfileView(RestaurantRequiredMixin, generic.FormView):
    model = Textiles
    template_name = "main/restaurant_profile.html"
    success_url = reverse_lazy("main:index")

    def get_form(self, form_class=None):
        if Textiles.objects.filter(user=self.request.user).exists():
            return RestaurantEditForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=Textiles.objects.get(user=self.request.user),
            )
        else:
            return RestaurantEditForm(self.request.POST or None, self.request.FILES or None)

    def form_valid(self, form):
        data = form.save()
        data.user = self.request.user
        data.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("data is not saved", form.errors)
        return super().form_invalid(form)


class RestaurantIndexView(RestaurantRequiredMixin, generic.ListView):
    context_object_name = "products"
    paginate_by = 50
    template_name = "main/restaurant_index.html"

    def get_queryset(self):
        return Product.objects.filter(subcategory__category__restaurant=Textiles.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        restaurant = Textiles.objects.get(user=self.request.user)
        category_count = Category.objects.filter(restaurant=restaurant).count()
        subcategory_count = Subcategory.objects.filter(category__restaurant=restaurant).count()
        product_count = Product.objects.filter(subcategory__category__restaurant=restaurant).count()
        context["restaurant"] = restaurant
        context["category_count"] = category_count
        context["subcategory_count"] = subcategory_count
        context["product_count"] = product_count
        return context


class RestaurantListView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    template_name = "main/restaurant_list.html"
    context_object_name = "restaurants"
    paginate_by = 50

    def get_queryset(self):
        return Textiles.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Textiles"
        return context


class RestaurantDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    model = Textiles
    template_name = "main/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Restaurant"
        return context


class RestaurantUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Textiles
    template_name = "main/restaurant_update.html"
    form_class = RestaurantEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Restaurant"
        return context

    def get_success_url(self):
        return reverse_lazy("main:restaurant_list")


class RestaurantCreateView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    model = Textiles
    template_name = "main/restaurant_create.html"
    form_class = RestaurantCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Restaurant"
        return context


class CategoryListView(RestaurantRequiredMixin, generic.ListView):
    template_name = "main/category_list.html"
    context_object_name = "categories"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Category.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categories"
        return context


class CategoryDetailView(RestaurantRequiredMixin, generic.DetailView):
    template_name = "main/category_detail.html"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Category.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categories"
        return context


class CategoryCreateView(RestaurantRequiredMixin, generic.CreateView):
    model = Category
    template_name = "main/category_create.html"
    fields = ("name", "image", "description")
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        data = form.save(commit=False)
        data.restaurant = Textiles.objects.get(user=self.request.user)
        data.save()
        return super().form_valid(form)


class CategoryUpdateView(RestaurantRequiredMixin, UpdateView):
    model = Category
    template_name = "main/category_update.html"
    fields = ("name", "image", "description")

    def dispatch(self, request, *args, **kwargs):
        if not Category.objects.get(pk=kwargs["pk"]).restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class CategoryDeleteView(RestaurantRequiredMixin, DeleteView):
    model = Category
    template_name = "main/category_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not Category.objects.get(pk=kwargs["pk"]).restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class SubcategoryListView(RestaurantRequiredMixin, generic.ListView):
    template_name = "main/subcategory_list.html"
    context_object_name = "subcategories"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Subcategory.objects.filter(category__restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categories"
        return context


class SubcategoryCreateView(RestaurantRequiredMixin, generic.CreateView):
    model = Subcategory
    template_name = "main/subcategory_create.html"
    fields = ("name", "description")

    def form_valid(self, form):
        category_pk = self.kwargs.get("category_pk")
        category = get_object_or_404(Category, pk=category_pk)
        data = form.save(commit=False)
        data.category = category
        data.save()
        return super().form_valid(form)

    def get_success_url(self):
        category_pk = self.kwargs.get("category_pk")
        category = get_object_or_404(Category, pk=category_pk)
        return category.get_absolute_url()


class SubcategoryUpdateView(RestaurantRequiredMixin, UpdateView):
    model = Subcategory
    template_name = "main/subcategory_update.html"
    fields = ("name", "description")

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().category.restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class SubcategoryDeleteView(RestaurantRequiredMixin, DeleteView):
    model = Subcategory
    template_name = "main/subcategory_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().category.restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class ProductListView(RestaurantRequiredMixin, generic.ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Product.objects.filter(subcategory__category__restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products"
        return context


class ProductDetailView(RestaurantRequiredMixin, generic.DetailView):
    template_name = "main/product_detail.html"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Product.objects.filter(subcategory__category__restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products"
        return context


class ProductCreateView(RestaurantRequiredMixin, generic.CreateView):
    model = Product
    template_name = "main/product_create.html"
    fields = ("subcategory", "name", "description", "image" , "is_popular")
    success_url = reverse_lazy("main:index")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['subcategory'].queryset = Subcategory.objects.filter(category__restaurant__user=self.request.user)
        return form


class ProductUpdateView(RestaurantRequiredMixin, UpdateView):
    model = Product
    template_name = "main/product_update.html"
    fields = ("subcategory", "name", "description", "image", "is_popular")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['subcategory'].queryset = Subcategory.objects.filter(category__restaurant__user=self.request.user)
        return form

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().subcategory.category.restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class ProductDeleteView(RestaurantRequiredMixin, DeleteView):
    model = Product
    template_name = "main/product_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().subcategory.category.restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class AddCartView(View):
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context = {'cart_items': cart_items, 'total_price': total_price}
        return render(request, 'web/includes/cart.html', context)

    def post(self, request, *args, **kwargs):
        option_pk = request.POST.get('option_pk')
        quantity = request.POST.get('quantity')
        session_key = request.session.session_key

        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key, product_id=option_pk, defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return JsonResponse({"message": "Item added to cart successfully"})


class MinusCartView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            option = Option.objects.get(pk=pk)
            session_key = request.session.session_key
            try:
                cart_item = CartItem.objects.get(session_key=session_key, option=option)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

                return JsonResponse({'message': 'Product removed from cart successfully'})
            except CartItem.DoesNotExist:
                return JsonResponse({'message': 'Product not found in cart'}, status=404)
        except Option.DoesNotExist:
            return JsonResponse({'message': 'Product option does not exist'}, status=404)


class HowItWorksView(generic.DetailView):
    template_name = "web/howitworks.html"
    context_object_name = "restaurant"
    model = Textiles


class NotificationListView(RestaurantRequiredMixin, generic.ListView):
    template_name = "main/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Notification.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notifications"
        return context


class NotificationDetailView(RestaurantRequiredMixin, generic.DetailView):
    template_name = "main/notification_detail.html"
    paginate_by = 50

    def get_queryset(self):
        restaurant = Textiles.objects.get(user=self.request.user)
        return Notification.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notifications"
        return context


class NotificationCreateView(RestaurantRequiredMixin, generic.CreateView):
    model = Notification
    template_name = "main/notification_create.html"
    fields = ("notification",)
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        data = form.save(commit=False)
        data.restaurant = Textiles.objects.get(user=self.request.user)
        data.save()
        return super().form_valid(form)


class NotificationUpdateView(RestaurantRequiredMixin, UpdateView):
    model = Notification
    template_name = "main/notification_update.html"
    fields = ("notification",)

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.save(commit=False)
        data.restaurant = Textiles.objects.get(user=self.request.user)
        data.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("main:index")


class NotificationDeleteView(RestaurantRequiredMixin, DeleteView):
    model = Notification
    template_name = "main/notification_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:index")


class OptionDeleteView(RestaurantRequiredMixin, DeleteView):
    model = Option
    template_name = "main/option_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().product.subcategory.category.restaurant.user == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("main:product_detail", kwargs={"pk": self.get_object().product.pk})


class OptionCreateView(RestaurantRequiredMixin, generic.CreateView):
    model = Option
    template_name = "main/option_create.html"
    fields = ("name", "price","org_price",)

    def get_success_url(self):
        product_pk = self.kwargs.get("product_pk")
        return reverse_lazy("main:product_detail", kwargs={"pk": product_pk})

    def form_valid(self, form):
        data = form.save(commit=False)
        product_pk = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_pk)
        data.product = product
        data.save()
        return super().form_valid(form)

