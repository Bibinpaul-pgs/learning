from django.shortcuts import render
# from asyncio import mixins
from rest_framework import generics
from rest_framework import mixins
from testapp.serializers import StudentSerializer
from testapp.models import Student
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

# class StudentGeneric(generics.GenericAPIView,
#                     mixins.ListModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.RetrieveModelMixin,
#                     mixins.DestroyModelMixin):
#     serializer_class = StudentSerializer
#     queryset = Student.objects.all()
#     lookup_field = 'id'

class StudentGeneric(generics.CreateAPIView, generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Student Creation failed"}

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'message: Student created successfully.'
     
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class FilterView(APIView):

    def post(self, request):

        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book not available"}

            from_age = request.data['from']
            to_age = request.data['to']
            data = Student.objects.filter(age__range=[from_age,to_age])
            # print(instance)
            age_list = []
            for ages in data:
                data = ages.name
            
                age_list.append(data)
                
                response["status"] = status.HTTP_200_OK
                response["data"] = age_list
                response["message"] = 'Book is Available'
            print(age_list)
          
            return Response(response)
            
                # else:
                #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print('Exception Occured',e)