from rest_framework.serializers import ModelSerializer
from table.models import WholeVocab


class WholeVocabSerializer(ModelSerializer):
    class Meta:
        model = WholeVocab
        fields = '__all__'