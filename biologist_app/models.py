from django.db import models
from django.utils.text import slugify


# ==============================
# CATEGORY
# ==============================
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==============================
# SUBCATEGORY
# ==============================
class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("category", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.category.name} → {self.name}"


# ==============================
# PRODUCT
# ==============================
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT
    )

    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_new = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==============================
# PRODUCT VARIANT  ✅ FIXED
# ==============================
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="variants",
        on_delete=models.CASCADE
    )

    # 🔥 FIXED LENGTH (was 50)
    catalog_number = models.CharField(
        max_length=255,
        unique=True
    )

    # 🔥 FIXED LENGTHS
    quantity = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["quantity"]

    def __str__(self):
        return f"{self.product.name} [{self.catalog_number}]"


# ==============================
# ENQUIRY
# ==============================
from django.db import models
from django.utils.text import slugify


# ==============================
# CATEGORY
# ==============================
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==============================
# SUBCATEGORY
# ==============================
class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("category", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.category.name} → {self.name}"


# ==============================
# PRODUCT
# ==============================
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT
    )

    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_new = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==============================
# PRODUCT VARIANT  ✅ FIXED
# ==============================
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="variants",
        on_delete=models.CASCADE
    )

    # 🔥 FIXED LENGTH (was 50)
    catalog_number = models.CharField(
        max_length=255,
        unique=True
    )

    # 🔥 FIXED LENGTHS
    quantity = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["quantity"]

    def __str__(self):
        return f"{self.product.name} [{self.catalog_number}]"


# ==============================
# ENQUIRY
# ==============================
class Enquiry(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="enquiries",
        on_delete=models.CASCADE
    )

    variant = models.ForeignKey(
        ProductVariant,
        related_name="enquiries",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} → {self.variant.catalog_number}"


# ==============================
# TEAM MEMBER
# ==============================
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.role}"


# ==============================
# TEAM MEMBER
# ==============================
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.role}"
