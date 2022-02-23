from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('userinfo', views.UserView, 'userinfo')
router.register('login', views.LoginView, 'login')

urlpatterns = [

]
urlpatterns += router.urls
