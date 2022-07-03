from django.urls import path
from . import views
from .views import PostEdit, PostNew, PostSearch, PostDelete, LogIn, SignUp, ChangePassword, PostDraft
from .views import PostView
from .views import PostDetail

# urlpatterns = [
#     path('', views.post_list, name='post_list'),
#     path('post/<int:pk>/', views.post_detail,name='post_detail'),
#     path('post/new/', views.post_new, name='post_new'),
#     path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
# ]

urlpatterns = [
    path('', PostView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetail.as_view(),name='post_detail'),
    path('post/new/', PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='post_delete'),
    path('myposts/', PostDraft.as_view(), name='my_posts'),
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('accounts/password_change/', ChangePassword.as_view(template_name='changepass.html', success_url='/'), name='change_password'),
    path('accounts/password_change/done/', PostView.as_view(), name='pass_done')
]

