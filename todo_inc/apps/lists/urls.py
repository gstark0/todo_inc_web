from django.urls import path
from . import views
from . import api

urlpatterns = [
	path('', views.show_lists),
	path('<str:code>/', views.render_list),
	path('api/lists/<str:code>', api.specific_list),
	path('api/lists', api.general_lists)
]