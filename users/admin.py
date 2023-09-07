from django.contrib import admin
from users.models import User
from products.admin import BasketAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-is_staff',)
    inlines = (BasketAdmin,)
