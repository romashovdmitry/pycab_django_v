from rest_framework.serializers import ModelSerializer
from table.models import Vocab


class WholeVocabSerializer(ModelSerializer):
    class Meta:
        model = Vocab
        fields = '__all__'