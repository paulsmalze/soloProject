from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('dashboard',views.dashboard),
    path('logout',views.logout),
    path('create',views.create),
    path('new', views.new),
    path('dashboard/<int:movie_id>/edit',views.edit),
    path('dashboard/<int:movie_id>/update',views.update),
    path('dashboard/<int:movie_id>',views.movie),
    path('dashboard/<int:movie_id>/delete',views.delete),
    path('dashboard/<int:movie_id>/like',views.add_like),
    # path('favorite/<int:movie_id>',views.favorite)
]