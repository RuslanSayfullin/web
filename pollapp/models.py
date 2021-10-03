from django.db import models


class Poll(models.Model):
    """Создание опроса"""
    poll_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    end_date = models.DateTimeField()
    poll_description = models.CharField(max_length=200)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    """Вопросы к опросу"""
    survey = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Изменение вопроса"""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    """Ответы к опросу"""
    user_id = models.IntegerField()
    survey = models.ForeignKey(Poll, related_name='survey', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.choice_text
