
from rest_framework import serializers 

from django.contrib.auth.models import User

from library.models import Book, IssueBook


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):

   

    class Meta:
        model = IssueBook
        fields = ["book", "user", "issue_date", "return_date", "status"]


