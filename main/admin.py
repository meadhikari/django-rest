from django.contrib import admin
from main.models import Binary
# Register your models here.

class BinaryAdmin(admin.ModelAdmin):
    #Maybe get all landing pages last known ecpc?
    list_display = ('title', 'file','default')
    list_editable = ('default',)
admin.site.register(Binary, BinaryAdmin)
