"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, EventGamer
from rest_framework.decorators import action


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        try: 
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(uid=request.data["uid"])
        game = Game.objects.get(pk=request.data["game"])
        
        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=organizer,
            game=game
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        EventGamer.objects.create(
            gamer = gamer,
            event = event,
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        eventgamer = EventGamer.objects.get(
            gamer = gamer,
            event = event,
        )
        eventgamer.delete()
        return Response({'message': 'Gamer removed'}, status=status.HTTP_201_CREATED)
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 1
