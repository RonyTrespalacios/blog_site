from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'
# Define un espacio de nombres para las URLs de la aplicación, 
# lo que facilita la referencia a las vistas en los templates 
# utilizando {% url 'blog:name' %}.

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:id>/edit/', views.post_update, name='post_update'),
    path('post/<int:id>/delete/', views.post_delete, name='post_delete'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Agregamos las vistas de login y logout
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    # Vista para registrar nuevos usuarios
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
