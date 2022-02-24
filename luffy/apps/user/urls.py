from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user_info', views.UserView, 'userinfo')
router.register('login', views.LoginView, 'login')
router.register('register', views.RegisterView, 'register')
urlpatterns = [

]
urlpatterns += router.urls
