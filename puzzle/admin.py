from django.contrib import admin

from .models import Hunt, Puzzle, Hint, Session, CustomUser, Guess

# Register your models here.
admin.site.register(Hunt)
admin.site.register(Puzzle)
admin.site.register(Hint)
admin.site.register(Session)
admin.site.register(CustomUser)
admin.site.register(Guess)

