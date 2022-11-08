from rest_framework.decorators import api_view
from rest_framework.response import Response
from table.models import WholeVocab
from .serializers import WholeVocabSerializer

@api_view(['GET'])
def get_words(request):
    words = WholeVocab.objects.all()
    words = WholeVocabSerializer(words, many=True)
    return Response(words.data)
