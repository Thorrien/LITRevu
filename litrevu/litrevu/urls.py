"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import application.views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.first_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('flux/', application.views.flux, name='flux'),
    path('signup/', authentication.views.singup_page, name='signup'),
    path('ticket/creation/', application.views.ticket_creation,
         name='ticketcreation'),
    path('ticket/<int:id>/change/', application.views.ticket_modify,
         name='ticketmodify'),
    path('ticket/<int:id>/delete/', application.views.ticket_delete,
         name='ticketdelete'),
    path('review/creation/', application.views.review_creation,
         name='reviewcreation'),
    path('review/<int:id>/change/', application.views.review_modify,
         name='reviewmodify'),
    path('review/<int:id>/delete/', application.views.review_delete,
         name='reviewdelete'),
    path('review/follow/', application.views.add_user_follow,
         name='followUsers'),
    path('review/follow/<int:id>/delete/',
         application.views.delete_user_follow,
         name='deletefollowUsers'),
    path('ticketReview/creation/', application.views.ticket_Review_creation,
         name='ticketreviewcreation'),
    path('create_review/<int:ticket_id>/',
         application.views.create_review_from_ticket,
         name='createreview'),
    path('posts/', application.views.fluxperso, name='fluxperso'),
    path('block_user/<int:user_id>/',
         application.views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/',
         application.views.unblock_user, name='unblock_user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
