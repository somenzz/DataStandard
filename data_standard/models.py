from django.db import models
from django.conf import settings
# Create your models here.

class StandardDict(models.Model):
    #属性中文名称
    attribute_ch_name = models.CharField(max_length=255,primary_key=True) 
    #属性代码值
    attribute_code = models.CharField(max_length=500) 
    #属性英文名称
    attribute_en_name = models.CharField(max_length=500) 
    #属性中文说明
    attribute_ch_desc = models.TextField(blank = True, null = True) 
    #属性值域说明
    attribute_val_dmn = models.TextField(blank = True, null = True) 
    #创建人员
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #创建时间
    create_time = models.DateTimeField(auto_now = True, null = False)
    #创建人员
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
