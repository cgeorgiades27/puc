from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.workout_log, name = 'workout_log'),
    path('log/<int:pk>', views.log_detail, name = 'log_detail'),
    path('log/new/', views.log_new, name = 'log_new'),
    path('user_id/<int:user_id>', views.user_logs, name = 'user_logs'),
    path('competition', views.competition, name = 'competition'),
    path('competition_list', views.competition_list, name = 'competition_list'),
    path('comp_entry/<int:compName_id>', views.comp_entry, name = 'comp_entry'),
    path('profile', views.profile, name = 'profile'),
    path('update_profile', views.update_profile, name = 'update_profile'),
    url('login', auth_views.LoginView.as_view(), name='login'),
    url('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('all_logs', views.all_logs, name = 'all_logs'),
    path('new_workout', views.new_workout, name = 'new_workout'),
    path('user_id_all/<int:user_id>', views.all_user_logs, name = 'all_user_logs'),
    #path('url/new/', views.user_settings, name = 'user_settings'),
]