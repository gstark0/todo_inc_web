from django.urls import path
from . import views

urlpatterns = [
	path('', views.show_lists),
	path('<str:code>/', views.render_list)
]