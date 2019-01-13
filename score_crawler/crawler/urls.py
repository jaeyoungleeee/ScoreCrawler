from django.urls import path
from .views import MainView, MemberDetailView


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('<str:name>/', MemberDetailView.as_view(), name='member_detail')
]
