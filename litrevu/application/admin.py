from django.contrib import admin
from application.models import Ticket, Review, UserFollows, UserBlock

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
admin.site.register(UserBlock)
