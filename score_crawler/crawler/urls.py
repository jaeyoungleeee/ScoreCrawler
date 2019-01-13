from django.urls import path
from .views import MainView


urlpatterns = [
    path('', MainView.as_view(), name='main')
    # path('/<string:user_name>/', ),
]
