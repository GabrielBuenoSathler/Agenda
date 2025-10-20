from django.contrib import admin

from contact import models 
# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
     list_display = 'id','first_name', 'last_name','phone','show'
     ordering = '-id',  
     list_filter = 'created_date',
     list_editable = 'show',
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',

