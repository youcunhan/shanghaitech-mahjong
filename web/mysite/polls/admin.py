from django.contrib import admin

# Register your models here.
from .models import Question
from .models import User
from .models import Battle
admin.site.register(Question)
admin.site.register(User)
admin.site.register(Battle)