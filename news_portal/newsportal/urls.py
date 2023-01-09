from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', cache_page(10)(PostDetail.as_view()), name='post_detail'),
   path('search', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]