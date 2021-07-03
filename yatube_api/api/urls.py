from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v2 = SimpleRouter()
router_v2.register('posts', PostViewSet)
router_v2.register('comments', CommentViewSet)
router_v2.register('group', GroupViewSet)
router_v2.register('follow', FollowViewSet)

urlpatterns = [
    path('', include(router_v2.urls)),
    path('posts/<int:post_id>/', include(router_v2.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
