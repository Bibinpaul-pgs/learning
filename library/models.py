
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    image = models.ImageField(upload_to="files",null=True,blank=True)
    files = models.FileField(upload_to="files",null=True,blank=True)

    class Meta:
        unique_together = ('title', 'author',)


class IssueBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    # current_date = models.DateField(null=True, blank=True)
    status = (
        ('issued', 'issued'),
        ('returned', 'returned'))
    status = models.CharField(choices=status, default="issued", max_length=20)

    class Meta:
        unique_together = ('book', 'user', 'status')
