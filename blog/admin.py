from operator import truediv
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)

class MyModelAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj):
        if request.user.is_superuser():
            return True
        elif request.user == obj.author:
            return True
        return False
    
    def has_delete_permission(self, request, obj):
        if request.user.is_superuser():
            return True
        elif request.user == obj.author:
            return True
        return False
    