from django.urls import path
from data_standard import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

app_name = 'data_standard'

urlpatterns = [
    path('standard_dict/',views.StandardDictList.as_view(),name='standard_dict'),
    path('standard_dict/<str:pk>/',views.StandardDictDetail.as_view(),name='standard_dict_detail'),
    path('', TemplateView.as_view(template_name="data_standard/auto_create_sql.html"), name='index'),
    path('auto', TemplateView.as_view(template_name="data_standard/data_standard_index.html"), name='auto'),
    path('autosql/', views.AutoSql.as_view(), name='sql'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
