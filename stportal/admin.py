from django.contrib import admin
from .models import CustomUser,ApplicationModel

# admin.site.register(CustomUser)
class ApplicationInline(admin.TabularInline):
    model = ApplicationModel

class CustomUserAdmin(admin.ModelAdmin):
    list_display=('id','first_name','last_name','email','password','is_active','role','is_staff')
    inlines=[ApplicationInline]

class ApplicationAdmin(admin.ModelAdmin):
    list_display=('app_id','uni_name','program_name','study_mode','customer','status')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(ApplicationModel,ApplicationAdmin)
