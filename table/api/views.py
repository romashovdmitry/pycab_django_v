from rest_framework.decorators import api_view
from rest_framework.response import Response
from table.models import WholeVocab
from .serializers import WholeVocabSerializer
from sys import path
from rest_framework import generics

path.append('../table')
from table.models import WholeVocab
from table.backendAndTelegram.sql_transactions import SQLTransactions as sqlt

@api_view(['GET'])
def get_words(request):
    words = WholeVocab.objects.all()
    words = WholeVocabSerializer(words, many=True)
    return Response(words.data)

@api_view(['POST'])
def post_new_word(request):
    test = sqlt(telegram_id=123).validateUserInTable()
    return Response({'way': test})

class WordsApiView(generics.RetrieveAPIView):
    queryset = WholeVocab.objects.all()
    serializer_class = WholeVocabSerializer