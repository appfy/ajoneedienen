from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class State(BaseModel):
    name = models.CharField("State Name", max_length=50)

    def __str__(self):
        return self.name


class District(BaseModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField("State Name", max_length=50)

    def __str__(self):
        return f"{self.state} - {self.name}"


class Textiles(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={"is_staff": True}, blank=True, null=True
    )
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="restaurant_logos", blank=True, null=True)
    phone = models.CharField(max_length=200, help_text="Phone number with country code")
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField()
    is_blocked = models.BooleanField(default=False)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    youtube_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)

    feature_image = models.ImageField(upload_to="restaurant/feature_images/",null=True, blank=True)
    feature_description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Textiles"

    def get_absolute_url(self):
        return reverse("main:restaurant_detail", kwargs={"pk": self.pk})

    def get_web_url(self):
        return reverse("web:restaurant_catalogue", kwargs={"pk": self.pk})

    def get_categories(self):
        return Category.objects.filter(restaurant=self)

    def get_populars(self):
        return Product.objects.filter(subcategory__category__restaurant=self, is_popular=True)
    
   

    def __str__(self):
        return self.name


class DefaultCategory(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Default Categories"


class Category(BaseModel):
    restaurant = models.ForeignKey(Textiles, on_delete=models.CASCADE , verbose_name="Textiles")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_web_url(self):
        return reverse("web:category_catalogue", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("main:category_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("main:category_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("main:category_delete", kwargs={"pk": self.pk})

    def get_subcategories(self):
        return Subcategory.objects.filter(category=self)

    def get_products(self):
        return Product.objects.filter(subcategory__category=self)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"


class Subcategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse("main:subcategory_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("main:subcategory_delete", kwargs={"pk": self.pk})

    def get_products(self):
        return Product.objects.filter(subcategory=self)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Subcategories"


class Product(BaseModel):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # ingredients = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    is_popular = models.BooleanField(default=True)
    # is_vegetarian = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name



    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("main:product_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("main:product_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("main:product_delete", kwargs={"pk": self.pk})

    def get_options(self):
        return Option.objects.filter(product=self)


class Option(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    org_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,help_text='cut this price')


    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def get_delete_url(self):
        return reverse("main:option_delete", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("product", "price")
        verbose_name_plural = "Options"


class Banner(models.Model):
    restaurant = models.ForeignKey(Textiles, on_delete=models.CASCADE , verbose_name="Textiles")
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return str(self.restaurant.name)


class CatalogueAd(models.Model):
    image = models.ImageField(upload_to='catalogue/ads/')
    display_upto = models.DateField()
    display_in = models.ManyToManyField(Textiles, blank=True)

    def __str__(self):
        return f"Advertisement: {self.image.url}"




class ProductAd(models.Model):
    image = models.ImageField(upload_to='product/ads/')
    display_upto = models.DateField()
    display_in = models.ManyToManyField(Textiles, blank=True)

    def __str__(self):
        return f"Advertisement: {self.image.url}"


class CartItem(models.Model):
    restaurant = models.ForeignKey(Textiles, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=200)
    product = models.ForeignKey(Option, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Notification(models.Model):
    restaurant = models.ForeignKey(Textiles, on_delete=models.CASCADE , verbose_name="Textiles")
    notification = models.TextField()

    def get_absolute_url(self):
        return reverse("main:notification_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("main:notification_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("main:notification_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.notification)


