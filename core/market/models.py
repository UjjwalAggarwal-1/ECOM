from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Category, self).save(*args, **kwargs)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Item Name", max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    seller = models.ForeignKey('users.Seller',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='items')

    class Meta:
        unique_together = ('name', 'seller')

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    
    def image_directory_path(self, filename):
        return 'item_images/{0}/{1}'.format(self.item.id, filename)
    
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return self.item.name + self.image.name


class Order(models.Model):

    status_choices = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('users.Customer', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.name


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, default='Pending')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.item.name