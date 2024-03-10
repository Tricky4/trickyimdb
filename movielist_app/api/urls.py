from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movielist_app.api.views import (WatchListAV, WatchDetailAV, 
                                     StreamListAV, StreamDetailAV, 
                                     ReviewList, ReviewDetail, ReviewCreate,
                                     StreamList, UserReview, WatchListGV)

router = DefaultRouter()
router.register('stream', StreamList, basename='streamlist')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watch-detail'),
    
    path('list2/', WatchListGV.as_view(), name='movie-list'),
    
    path('', include(router.urls)),
    
    # path('stream/', StreamListAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamDetailAV.as_view(), name='streamplatform-detail'),    
    
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    # path('review/', ReviewList.as_view(), name='review-list')
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    path('reviews/', UserReview.as_view(), name='user-review-detail')
]

# urlpatterns = [
#     path('list/', movie_list, name='movie-list'),
#     path('<int:pk>', movie_details, name='movie-detail'),
# ]
