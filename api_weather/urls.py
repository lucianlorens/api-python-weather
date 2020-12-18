from django.urls import include, path
from rest_framework import routers
from api_weather.control_panel import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'status', views.StatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('locations/', views.locations_list, name='locations'),
    path('locations/<int:pk>', views.locations_detail, name='locations_detail'),
    path('locations/<int:location_pk>/parameters/', views.parameters_list, name = 'parameters')),
    path('locations/<int:location_pk>/parameters/<int:parameter_pk>', views.parameters_detail, name = 'parameters_detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('status/', include()),
    
]
