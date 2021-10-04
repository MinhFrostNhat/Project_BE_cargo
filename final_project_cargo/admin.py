
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as ABCXYZ
from .models import User_inf, Send_cargo

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.exceptions import PermissionDenied


admin.site.site_header = "Let's go admin control "
admin.site.disable_action('delete_selected')

admin.site.index_title = 'Staff control manage area'


@receiver(pre_delete, sender=User_inf)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied('ss')


@admin.register(User_inf)
class Useradmin(ABCXYZ):
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'phone_number', 'group')
    exclude = ('password',)
    readonly_fields = ('username',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Send_cargo)
class Send_cargo_admin(admin.ModelAdmin):
    fields = (
        'id', 'driver', 'rider', 'pick_up_address', 'drop_off_address', 'status',

        'create_work', 'update_work', 'cargo_weight', 'cargo_note', 'phone_number_get_cargo', 'get_cargo_name',
    )

    list_display = (
        'id', 'driver', 'rider', 'phone_number_get_cargo',

        'get_cargo_name', 'pick_up_address', 'drop_off_address', 'status', 'cargo_price', 'cargo_distance',

        'cargo_weight', 'cargo_note', 'create_work', 'update_work',
    )
    list_filter = (
        'status',
    )
    readonly_fields = (
        'id', 'create_work', 'update_work',
    )
    ordering = ['-update_work']
    search_fields = ['status', 'phone_number_get_cargo',
                     'get_cargo_name', ]
