from rest_framework import serializers
from testapp.models import Student

class StudentSerializer(serializers.ModelSerializer):

        


    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, data):
        age = data.get("age")
        if age<15:
            raise serializers.ValidationError("age is low")
        return data
