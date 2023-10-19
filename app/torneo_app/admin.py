from django.contrib import admin

from torneo_app.models import *
from users.admin import CustomUserAdmin

# admin.site.register(Discipline, CustomUserAdmin)
# admin.site.register(Tournament, CustomUserAdmin)
# admin.site.register(Sponsor, CustomUserAdmin)
# admin.site.register(Result, CustomUserAdmin)
# admin.site.register(TournamentAssignment, CustomUserAdmin)

admin.site.register(Discipline)
admin.site.register(Tournament)
admin.site.register(Sponsor)
admin.site.register(Result)
admin.site.register(TournamentAssignment)
