from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_log, name = 'workout_log'),
    path('log/<int:pk>', views.log_detail, name = 'log_detail'),
    path('log/new/', views.log_new, name = 'log_new'),
    path('user_id/<int:user_id>', views.user_logs, name = 'user_logs'),
    path('competition', views.competition, name = 'competition'),
    #path('<int:user_id>/<int:workout_title')
    #path('url/new/', views.user_settings, name = 'user_settings'),
]