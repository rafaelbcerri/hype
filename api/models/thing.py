from mongoengine import *
from django.utils import timezone

class Thing(Document):
  meta = {'collection': 'things'}

  text = StringField(max_length=200, default="")
  date = DateTimeField(default=timezone.now)
  sub_things = ListField(StringField(max_length=200))

  def __str__(self):
    return self.text
