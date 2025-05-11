from django.urls import path
from .views import hello_api, submit_form, register_user, get_daily_horoscope,mbti_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path('hello/', hello_api, name='hello_api'),
    path('submit/', submit_form, name='submit_form_alt'),
    path('register/', register_user, name='register_user'), 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('horoscope/', get_daily_horoscope, name='get_daily_horoscope'),
    path('mbti/', mbti_view, name='mbti'),

    # 處理根路徑，返回首頁或一個簡單的訊息
    path('', TemplateView.as_view(template_name='index.html')),  # 這裡可以指向 Vue 的 index.html
]
