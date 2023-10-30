from django.contrib import admin
from .models import Hunt, Puzzle, Hint, CustomUser

# Register your models here.
admin.site.register(Hunt)
admin.site.register(Puzzle)
admin.site.register(Hint)
admin.site.register(CustomUser)