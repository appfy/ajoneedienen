from django.urls import path

from . import views


app_name = "main"

urlpatterns = [
    path("registration/", views.UserRegisterView.as_view(), name="registration_register"),
    path("accounts/register/", views.UserRegisterView.as_view(), name="registration_register"),
    path("home/", views.IndexView.as_view(), name="index"),
    path("dash/admin/", views.AdminIndexView.as_view(), name="admin_index"),
    # profile - restaurant
    path("dash/Textiles/", views.RestaurantIndexView.as_view(), name="restaurant_index"),
    path("blocked/Textiles/", views.RestaurantBlockedView.as_view(), name="restaurant_blocked"),
    path("update/Textiles/", views.AutoRestaurantUpdateView.as_view(), name="auto_restaurant"),
    path("profile/Textiles/", views.RestaurantProfileView.as_view(), name="restaurant_update"),
    # Textiles - crud
    path("Textiles/", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("Textiles/new/", views.RestaurantCreateView.as_view(), name="restaurant_new"),
    path("Textiles/<str:pk>/", views.RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("Textiles/<str:pk>/edit/", views.RestaurantUpdateView.as_view(), name="restaurant_edit"),
    # notifications - crud
    path("notifications/", views.NotificationListView.as_view(), name="notification_list"),
    path("notifications/new/", views.NotificationCreateView.as_view(), name="notification_new"),
    path("notifications/<str:pk>/", views.NotificationDetailView.as_view(), name="notification_detail"),
    path("notifications/<str:pk>/edit/", views.NotificationUpdateView.as_view(), name="notification_edit"),
    path("notifications/<str:pk>/delete/", views.NotificationDeleteView.as_view(), name="notification_delete"),
    # categories - crud
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/new/", views.CategoryCreateView.as_view(), name="category_new"),
    path("categories/<str:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("categories/<str:pk>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<str:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
    # subcategories - crud
    path("subcategories/", views.SubcategoryListView.as_view(), name="subcategory_list"),
    path("subcategories/<str:category_pk>/new/", views.SubcategoryCreateView.as_view(), name="subcategory_new"),
    path("subcategories/<str:pk>/edit/", views.SubcategoryUpdateView.as_view(), name="subcategory_edit"),
    path("subcategories/<str:pk>/delete/", views.SubcategoryDeleteView.as_view(), name="subcategory_delete"),
    # products
    path("products", views.ProductListView.as_view(), name="product_list"),
    path("products/new/", views.ProductCreateView.as_view(), name="product_new"),
    path("products/<str:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<str:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("products/<str:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("cart/<str:pk>/add/", views.AddCartView.as_view(), name="add_to_cart"),
    path("cart/<str:pk>/minus/", views.MinusCartView.as_view(), name="minus_to_cart"),
    path("howitworks/<str:pk>/", views.HowItWorksView.as_view(), name="howitworks"),
    path("option/<str:product_pk>/new/", views.OptionCreateView.as_view(), name="option_new"),
    path("option/<str:pk>/delete/", views.OptionDeleteView.as_view(), name="option_delete"),
]
