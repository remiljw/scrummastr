from django.urls import include,path
from remiljscrumy import views

app_name = 'remiljscrumy'


urlpatterns = [
    path('',views.index,name='index'),
   

    path('<int:goal_id>/', views.move_goal, name = "move_goal"),

    path('accounts/', include('django.contrib.auth.urls')),
]



