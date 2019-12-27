from django.shortcuts import render
from logging import getLogger

# Create your views here.
from rest_framework.views import APIView
from data_standard.models import StandardDict
from data_standard.serializers import StandardDictSerializer
from rest_framework import generics,permissions
from .get_parameter import get_parameter_dic
from rest_framework.response import Response
from django.db.models.functions import Length
import jieba

# api 文档

from rest_framework.schemas import AutoSchema


## 增加一些自定义的词组
with open("userdict.txt","r",encoding='utf-8') as r:
   for line in r:
       word = line.strip() 
      ####print(word)
       jieba.add_word(word)
logger = getLogger()
data_type = {
0:'varchar',
1:'integer',
2:'decimal',
3:'timestamp',
4:'date',
5:'boolean'
}

def get_en_code(name):
   ####print(name)
    std = StandardDict.objects.filter(attribute_ch_name = name)
    if std:
        return std[0].attribute_code
    else:
        code = []
        for item in jieba.cut(name,cut_all = False):
            std = StandardDict.objects.filter(attribute_ch_name = item)
            if std:
                code.append(std[0].attribute_code)
            else:
                logger.info(f"{item} is not found")
               ####print(item)

        return "_".join(code)


class StandardDictList(generics.ListCreateAPIView):
    serializer_class = StandardDictSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = []
        obj = StandardDict.objects
        kw = self.request.query_params.get('kw', None)
       ####print(kw)
        if kw is not None:
            queryset = obj.filter(attribute_ch_name__contains = kw).order_by(Length('attribute_ch_name'))
        if queryset.count() == 0:
           ####print(kw[-1:])
            queryset = obj.filter(attribute_ch_name__startswith = kw[-1:]).order_by(Length('attribute_ch_name'))
           ####print(queryset)
              
        return queryset


class StandardDictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StandardDict.objects.all()
    serializer_class = StandardDictSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AutoSql(APIView):
    """
    自动建表
    """
    #permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        '''
        '''
        # 获取请求方的 ip 地址
        sql = ''
        #print(request.data)
        ip = ""
        return_data = {}
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        params = get_parameter_dic(request)
       ####print(params)
       ####print(type(params))
        # colname and tabname and where and redis_con.existsvalue(tabname.upper()):
        tabname_cn = params.get('name','')
        readme = params.get('readme','')
        pks = [] 
        tabname_code = f"TBL_{get_en_code(tabname_cn).replace('_TBL','')}"
        colname_fields_str = ""
        comment_fields_str = f"comment on table {tabname_code} is '{tabname_cn} {readme}';\n"
        for item in params.get('fields',[]):
            colname_code = get_en_code(item['name'])
            if item['type'] in [0,2]:
                length = item['length']
                if length == '':
                    if item['type'] == 0:
                        length = '60'
                    else:
                        length = '20,2'
                colname_type = f"{data_type[item['type']]}({length})"
            else:
                colname_type = data_type[item['type']]
            colname_fields_str += f"{colname_code} {colname_type} {'not null' if item['required'] else ''},\n"
            if item['is_pk']:
                pks.append(colname_code)
            comment_fields_str += f"comment on column {tabname_code}.{colname_code} is '{item['name']}"
            #增加码值信息
            if item['readme'] != '':
                comment_fields_str += f"[{item['readme']}]';\n"
            else:
                comment_fields_str += "';\n"
        if pks:
            colname_fields_str += f"constraint pk_{tabname_code} primary key ({','.join(pks)})"
        else:
            colname_fields_str = colname_fields_str[:-2]

              
            
        return_data['sql'] = f'''create table {tabname_code}(
{colname_fields_str}
)
/*
in tbs_data
index in tbs_index
*/
;
{comment_fields_str}
'''.lower()

        logger.info(f"user = {request.user} , ip = {ip}, create_sql = {sql}")
        return Response(return_data)

