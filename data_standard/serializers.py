from rest_framework import serializers
from data_standard.models import StandardDict


class StandardDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardDict
        fields = ['attribute_ch_name', 'attribute_code', 'attribute_en_name', 'attribute_ch_desc', 'attribute_val_dmn','create_user']
        #fields = '__all__'

