from django.contrib import admin

# Register your models here.
from application.models import Ticket, Review, UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
