from django.contrib import admin

from accounts.models import ItemModel, UserModel

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_active', 'is_verified', 'is_superuser')
    list_filter = ('is_active', 'is_verified', 'is_superuser', 'role')
    search_fields = ('email', 'username', 'phone_number')


@admin.register(ItemModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)