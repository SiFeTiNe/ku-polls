import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    """A Question model class."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def __str__(self):
        """Returns string question text of the Question object.

        Returns:
            A question text of this object.
        """
        return self.question_text

    def was_published_recently(self):
        """Returns boolean to check that was this object's question published recently.

        Returns True if this object's question was published less that or equal to 24 hours.
        Otherwise, Returns False.
        
        Returns:
            boolean to check was this published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Returns boolean to check that was this object's question published.

        Returns True if this object's question was published already.
        Otherwise, Returns False.

        Returns:
            boolean to check was this published.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Returns boolean to check that can this object's question be voted.

        Returns True if this object's question can be voted.
        Otherwise, Returns False.

        Returns:
            boolean to check that can this be voted.
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """A Choice model class."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Returns string choice text of the Choice object.

        Returns:
            A choice text of this object.
        """
        return self.choice_text
