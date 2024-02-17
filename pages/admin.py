"""Admin
"""

from django.contrib import admin

from pages.models import (
    Checkout,
    Costumer,
    Gym,
    GymUsage,
    Item,
    Pool,
    PoolUsage,
    RestaurantParchase,
    Room,
)

admin.site.register(Room)
admin.site.register(Checkout)
admin.site.register(Costumer)
admin.site.register(Item)
admin.site.register(RestaurantParchase)
admin.site.register(Gym)
admin.site.register(Pool)
admin.site.register(GymUsage)
admin.site.register(PoolUsage)
