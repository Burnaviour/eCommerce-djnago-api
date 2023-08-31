from django.db import models

# Create your models here.


class Collection(models.Model):

    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Promotions(models.Model):
    title = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    """_summary_

    Args:
        models (Product): "Product model store product related data"
    """
    title = models.CharField(max_length=255)
    # link which are query with dashes are slug
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotions)


class Customer(models.Model):
    BRONZE = 'B'
    SILVER = 'S'
    GOLD = 'G'
    MEMBER_SHIP = [(BRONZE, 'Bronze'), (SILVER, 'Silver'), (GOLD, 'Gold')]
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    member_ship = models.CharField(
        max_length=255, choices=MEMBER_SHIP, default=BRONZE)

    class Meta:
        indexes = [models.Index(fields=['first_name', 'last_name'])]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAILED = 'F'
    PAYMENT_CHOICES = [(PENDING, 'Pending'), (COMPLETE,
                                              'Complete'), (FAILED, 'Failed')]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PENDING)
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
