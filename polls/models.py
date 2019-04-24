from mongoengine import *
from django.utils import timezone


class Choice(EmbeddedDocument):
  text = StringField(max_length=200, default="")
  votes = IntField(default=0)

  def __str__(self):
    return self.text

class Question(Document):
  text = StringField(max_length=200, default="")
  date = DateTimeField(default=timezone.now)
  choices = ListField(EmbeddedDocumentField(Choice))

  class Meta:
    db_table = 'question'

  def __str__(self):
    return self.text



####
# import datetime

# from django.db import models
# from django.utils import timezone

# class Question(models.Model):
#   def __str__(self):
#     return self.question_text

#   def was_published_recently(self):
#     now = timezone.now()
#     one_day = datetime.timedelta(days=1)
#     return now - one_day <= self.pub_date <= now

#   was_published_recently.admin_order_field = 'pub_date'
#   was_published_recently.boolean = True
#   was_published_recently.short_description = 'Published recently?'

#   question_text = models.CharField(max_length=200)
#   pub_date = models.DateTimeField('date published')



# class Choice(models.Model):
#   def __str__(self):
#     return self.choice_text
#   question = models.ForeignKey(Question, on_delete=models.CASCADE)
#   choice_text = models.CharField(max_length=200)
#   votes = models.IntegerField(default=0)
