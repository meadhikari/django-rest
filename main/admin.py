from django.contrib import admin
from main.models import Binary,Profile,ImageProcessing
# Register your models here.

class BinaryAdmin(admin.ModelAdmin):
    #Maybe get all landing pages last known ecpc?
    list_display = ('title', 'file','default')
    list_editable = ('default',)
admin.site.register(Binary, BinaryAdmin)

class ProfileAdmin(admin.ModelAdmin):
    #Maybe get all landing pages last known ecpc?
    list_display = ('user', 'usage','limit')
    list_editable = ('limit',)
admin.site.register(Profile, ProfileAdmin)

class ImageAdmin(admin.ModelAdmin):
    #Maybe get all landing pages last known ecpc?
    list_display = ('image',)
admin.site.register(ImageProcessing, ImageAdmin)

