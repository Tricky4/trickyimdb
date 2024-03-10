from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import  IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters

from movielist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from movielist_app.models import (WatchList, StreamPlatform, Review)
from movielist_app.api.serializers import (WatchlistSerializer, 
                                           StreamPlatformSerializer, 
                                           ReviewSerializer)

from movielist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

from movielist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username = username)
    

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You already have reviewed this movie!")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        serializer.save(watchlist=movie, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-detail'
    

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchlistSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination
    
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchlistSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
         serializer = WatchlistSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchlistSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
    
class StreamList(viewsets.ModelViewSet):    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
        
# class StreamList(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def retrieve(self, request, pk=None):
#         instance = get_object_or_404(StreamPlatform, pk=pk)
#         serializer = StreamPlatformSerializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

#     def update(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        stream = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error: Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        stream = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# # Create your views here.
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.all()
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movies not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':    
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)