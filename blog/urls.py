from django.urls import path,register_converter,re_path
from .views import *
from .utils import *

register_converter(FourDigitYear,'fourdigit')

urlpatterns = [
    path('postlist/',PostList),
    path('detail/<int:idea>',PostDetail,name     = 'post_detail' ),
    path('listpost/<fourdigit:year>',PostListByYear),
    re_path(r"archive/(?P<year>[0-9]{2,4})/",ArchiveByYear),

]