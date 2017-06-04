from django.contrib import admin
from pproject.models import Car, CommonUser, CommentCarOwner, \
    CommentCar, CarType, FuelType, TrasmissionType, ConditionType


class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'title', 'view_birth_date')

admin.site.register(Car)
admin.site.register(CommonUser)
admin.site.register(CommentCarOwner)
admin.site.register(CommentCar)

admin.site.register(CarType)
admin.site.register(FuelType)
admin.site.register(TrasmissionType)
admin.site.register(ConditionType)
