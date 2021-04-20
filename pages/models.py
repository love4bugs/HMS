from django.db import models

class Room(models.Model):
    ROOM_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite')
    ]

    room_no = models.IntegerField(primary_key = True)
    empty = models.BooleanField(default=True)
    AC = models.BooleanField(default=False)
    room_type = models.CharField(max_length=10, choices=ROOM_CHOICES, default='Single')
    room_cost = models.IntegerField(default=1000)
    floor = models.IntegerField(default=1)

class Costumer(models.Model):
    GENERAL = 'N'
    SILVER = 'S'
    GOLD = 'G'
    PREMIUM = 'P'
    PACKAGE_CHOICES = [
        (GENERAL, 'General'),
        (SILVER, 'Sliver'),
        (GOLD, 'Gold'),
        (PREMIUM, 'Premium')
    ]

    name = models.CharField(max_length = 52)
    phone = models.CharField(max_length = 13)
    room_no = models.IntegerField()
    advance = models.IntegerField(default=100)
    checkin_time = models.DateTimeField(auto_now_add=True, blank=True)
    expected_checkout_time = models.DateField(blank=True, null=True)
    package = models.CharField(max_length=1, choices=PACKAGE_CHOICES, default=GENERAL)
    active = models.BooleanField(default=True)

    def get_package_cost(self):
        if self.package == 'S':
            return 500
        if self.package == 'G':
            return 2000
        if self.package == 'P':
            return 5000
        else:
            return 0
    
    def get_package_name(self):
        if self.package == 'S':
            return 'Sliver'
        if self.package == 'G':
            return 'Gold'
        if self.package == 'P':
            return 'Premium'
        else:
            return 'General'

        
class Checkout(models.Model):
    room_no = models.IntegerField()
    name = models.CharField(max_length = 52)
    phone = models.CharField(max_length = 13)
    checkout_time = models.DateTimeField(auto_now_add=True, blank=True)
    paid = models.BooleanField(default=False)
    consumer = models.ForeignKey(to=Costumer, on_delete=models.CASCADE, null=True)

class Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length=100)
    item_cost = models.IntegerField()

class RestaurantParchase(models.Model):
    consumer = models.ForeignKey(to=Costumer, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    qunatity = models.IntegerField()
    order_id = models.IntegerField()
    paid = models.BooleanField(default=False)

class Gym(models.Model):
    cost_per_hour = models.IntegerField()

class Pool(models.Model):
    cost_per_hour = models.IntegerField()

class GymUsage(models.Model):
    consumer = models.ForeignKey(to=Costumer, on_delete=models.CASCADE, null=True)
    gym = models.ForeignKey(to=Gym, on_delete=models.CASCADE)
    time_spent_in_hours = models.IntegerField()
    usage_id = models.IntegerField()
    paid = models.BooleanField(default=False)

class PoolUsage(models.Model):
    consumer = models.ForeignKey(to=Costumer, on_delete=models.CASCADE, null=True)
    pool = models.ForeignKey(to=Pool, on_delete=models.CASCADE)
    time_spent_in_hours = models.IntegerField()
    usage_id = models.IntegerField()
    paid = models.BooleanField(default=False)