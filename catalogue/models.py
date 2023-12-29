from django.db import models


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3

    ATTRIBUTE_TYPES_FIELDS = (
        (INTEGER, "Integer"),
        (STRING, "String"),
        (FLOAT, "Float"),
    )
    title = models.CharField(max_length=32)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='attributes')
    attributes_type = models.PositiveIntegerField(default=INTEGER, choices=ATTRIBUTE_TYPES_FIELDS)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products_types')
    upc = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products_cat')
    brand = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products_brand')

    def __str__(self):
        return self.title


class ProductAttributes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=48)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name='values')

    def __str__(self):
        return f"{self.product}({self.attribute}): {self.value}"

