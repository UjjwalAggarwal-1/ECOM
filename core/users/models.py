from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils import timezone


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    password = models.CharField(_("password"), max_length=128)
    email = models.EmailField(_("email address"), unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=1, null=True, blank=True, choices=(("M","Male"), ("F", "Female"), ("O", "Other")))

    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    def __str__(self):
        return str(self.id) + self.username


class Seller(User):
    total_sales = models.PositiveIntegerField(default=0)


class Customer(User):
    total_purchases = models.PositiveIntegerField(default=0)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE)
    items = models.ManyToManyField('market.Item')

    def __str__(self):
        return str(self.id) + self.customer.user.username


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    order_item = models.OneToOneField('market.OrderItem', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + self.order_item.item.name + self.order_item.order.customer.user.username