from django.contrib import admin

from torneo_app.models import *
from users.admin import CustomUserAdmin
from users.models import MyUser

admin.site.register(Tournament)
admin.site.register(Discipline)
admin.site.register(Sponsor)
admin.site.register(Result)
admin.site.register(TournamentAssignment)
