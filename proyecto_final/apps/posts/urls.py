from django.urls import path
from .views import PostListView, PostDetailView, DeletePostView, AddPostView,EditPostView

app_name = 'apps.posts'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='individual_post'),
    path('posts/<int:id>/delete', DeletePostView.as_view(), name='delete_post'),
    path('posts/add_post/', AddPostView.as_view(), name='add_post'),
    path('posts/edit/<int:id>', EditPostView.as_view(), name='edit_post'),
]
