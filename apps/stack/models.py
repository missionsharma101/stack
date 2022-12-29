from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    image = models.FileField(upload_to='uploads/%Y/%m/%d', null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Question(BaseModel):
    name = models.CharField(max_length=255)
    description=models.TextField(null=True)
    tag = models.CharField(max_length=100)
    upvote = models.IntegerField(blank=True, null=True)
    downvote = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.created_by.username + "/ " + self.name[0:20]


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.TextField()
    upvote = models.IntegerField(null=True, blank=True)
    downvote = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.question.name[0:20] + "/" + self.name[0:20]


class Reply(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self) -> str:
        return self.answer.name[0:20] + "/" + self.name[0:20]
