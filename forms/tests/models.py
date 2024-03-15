import uuid

from django.db import models


class Test(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=1000)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text


class Task(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=1_000)
    choises = models.ManyToManyField(Answer, blank=False,
                                     related_name='choises')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    true_ans = models.ForeignKey(Answer, on_delete=models.CASCADE,
                                 related_name='true_ans')

    def __str__(self):
        return self.text


class Results(models.Model):
    date = models.DateField(auto_now=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    res = models.JSONField()

