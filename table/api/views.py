from rest_framework.decorators import api_view
from rest_framework.response import Response
from table.models import Vocab
from .serializers import WholeVocabSerializer
from sys import path
from rest_framework import generics, authentication

path.append('../table')
from table.models import Vocab

@api_view(['GET'])
def get_words(request):
    words = Vocab.objects.all()
    words = WholeVocabSerializer(words, many=True)
    return Response(words.data)


@api_view(['POST'])
def post_new_word(request):
#    test = sqlt(telegram_id=123).validateUserInTable()
# check theres user ot not
    return Response({'way': None})

class WordsApiView(generics.RetrieveAPIView):
    queryset = Vocab.objects.all()
    serializer_class = WholeVocabSerializer


class createWord(generics.CreateAPIView):
    queryset = Vocab.objects.all()
    serializer_class = WholeVocabSerializer
    authentication_classes = [authentication.TokenAuthentication]