from django.contrib import admin
from .models import Kitten, Breed
from .models import UserToken

class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(Kitten)
admin.site.register(Breed)