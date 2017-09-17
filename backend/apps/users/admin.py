from django.contrib import admin
from django.contrib.auth import get_user_model

class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'first_name', 'middle_name', 'last_name')
    fields = ('email', 'first_name', 'middle_name', 'last_name', 'dob', 'is_active',
        'date_joined', 'date_updated')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('date_joined', 'date_updated')
        return self.readonly_fields


admin.site.register(get_user_model(), UserAdmin)
