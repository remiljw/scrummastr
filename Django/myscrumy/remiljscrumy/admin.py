from django.contrib import admin
from remiljscrumy.models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(GoalStatus)
admin.site.register(ScrumyHistory)
admin.site.register(ScrumyGoals)
admin.site.register(ScrumUser)
admin.site.register(ScrumProjectRole)
# admin.site.register(ScrumRole)

#admin.site.register(User)