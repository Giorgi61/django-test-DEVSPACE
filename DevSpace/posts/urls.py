from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [path('', views.PostsView.as_view(), name='all_posts'),
               path('<slug:slug>/<uuid:uuid>/', views.PostDetailView.as_view(), name='detail_post'),
               path('edit/<slug:slug>/<uuid:uuid>', views.PostEditView.as_view(), name='edit_post'),
               path('create/', views.PostCreateView.as_view(), name='create_post'),
               ]



'utf-8'

