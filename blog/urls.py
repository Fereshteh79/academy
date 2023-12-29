from django.urls import path, re_path, register_converter
from academy.blog.utils import FourDigityear
from academy.blog.views import categories_list, post_list, post_detail, costom_post_detail

register_converter(FourDigityear, 'four digit')

urlpatterns = [
    path('list/', post_list),
    path('detail/<int:post_id>/', post_detail),
    path('detail/<uuid:post_uuid>/', post_detail),
    path('detail/<slug:post_slug>/', post_detail),
    re_path(r"detail/(?P<post_slug>[\w-]+/)", post_detail),
    path('detail/hello/', costom_post_detail),
    path('categories/list/', categories_list),
    path('archive/<fourdigit:year>/', post_list),
    # re_path(r"archive/(?P<year>[0_9]{2,4})/", post_list),
    path('archive/<int:year>/int:month/', post_list),
    re_path(r'archive/(?P<code>[0_9]{4})/', post_list),
    re_path(r'archive/(?P<code>[0_9]{6})/', post_list),

]
