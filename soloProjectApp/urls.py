from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('dashboard',views.dashboard),
#     path('create',views.create),
#     path('new', views.new),
#     path('<int:movie_id>/edit',views.edit),
#     path('<int:movie_id>/update',views.update),
#     path('<int:movie_id>',views.movie),
#     path('<int:movie_id>/delete',views.delete),
#     path('logout',views.logout)
]