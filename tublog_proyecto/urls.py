from django.contrib.auth import views as auth_views
from tublog import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from tublog.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # ... Other URL patterns ...
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    path('logout/', views.user_logout, name='user_logout'),
    path('blogposts/', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('blogposts/create/', login_required(views.BlogPostCreateView.as_view()), name='blogpost_create'),
    path('blogposts/update/<int:pk>/', login_required(views.BlogPostUpdateView.as_view()), name='blogpost_update'),
    path('blogposts/delete/<int:pk>/', login_required(views.BlogPostDeleteView.as_view()), name='blogpost_delete'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('', views.home, name='home'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.category_list, name='category_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/', views.tag_list, name='tag_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('blogposts/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)