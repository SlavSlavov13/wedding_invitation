from django.urls import path
from . import views

urlpatterns = [
	path("invite/<str:slug>/", views.invitation_detail, name="invitation_detail"),
]