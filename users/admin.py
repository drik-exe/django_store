from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User, PasswordReset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-is_staff',)
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('code', 'email', 'expiration')
    fields = ('code', 'email', 'expiration', 'created')
    readonly_fields = ('created',)
