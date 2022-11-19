"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game_type


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        game_type = Game_type.objects.get(pk=pk)
        serializer = GameTypeSerializer(game_type)
        return Response(serializer.data)


    def list(self, request):
        game_types = Game_type.objects.all()
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)
      
class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game_type
        fields = ('id', 'label')
