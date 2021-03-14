from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images', blank=True,  null=True, default=None)
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name =  models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    status
        0: 注文受付中
        1: 注文受付完了
        2: 決済完了
        3: 受け取り完了
    """    
    customer = models.CharField(max_length=50)
    ordered_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.customer[:6]}:{self.ordered_at}'
class OrderDetail(models.Model):
    dish = models.ForeignKey(to=Dish, null=True, on_delete=models.SET_NULL)
    amount = models.SmallIntegerField()
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)