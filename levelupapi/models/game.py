from django.db import models
from .game_type import Game_type
from .gamer import Gamer

class Game(models.Model):

  game_type = models.ForeignKey(Game_type, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  maker = models.CharField(max_length=50)
  gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
  number_of_players = models.IntegerField()
  skill_level = models.CharField(max_length=50)
