
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from api.serializers import GroupSerializer, PostPublishSerializer, PostSerializer, UserSerializer, TagSerializer,CategorySerializer
from newspaper.models import Category, Post, Tag



from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.views import Response
from django.utils import timezone
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all().order_by('-id')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        
        return super().get_permissions()



class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset= super().get_queryset()
        if self.action in ["list","retrieve"]:
            queryset = queryset.filter(status="active", published_at__isnull=False)
            return queryset

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()



class PostPublishView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostPublishSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data

            # publish the post
            post = Post.objects.get(pk=data["id"])
            post.published_at = timezone.now()
            post.save()

            serialized_data = PostSerializer(post).data
            return Response(serialized_data, status=status.HTTP_200_OK)
    
class PostListByCategoryViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status = "active",
            published_at__isnull = False,
            category = self.kwargs["category_id"],
        )
        return queryset
    
class PostListByTagViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status = "active",
            published_at__isnull = False,
            tag = self.kwargs["tag_id"],
        )
        return queryset