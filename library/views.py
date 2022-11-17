from django.shortcuts import render
import datetime
from rest_framework import viewsets
from django.contrib.auth.models import User
from library.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import permissions, authentication
from library.tasks import *
from datetime import date, timedelta,datetime
from time import strftime
from library.serializers import BookSerializer, UserRegistrationSerializer, IssueSerializer
import logging, traceback
logger = logging.getLogger('django')

# Create your views here.



"""CRUD for Book """
class BookView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        try:


            today = datetime.now()
            print(today)
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Books Not Found"}
            issued_list = Book.objects.all()
            serializer = self.serializer_class(issued_list, many=True)

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Books Fetched Succesfully'
            
            logger.info('inside get books')
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            logger.error('not got into the books')
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book Creation Failed"}
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()

                response["status"] = status.HTTP_201_CREATED
                response["data"] = serializer.data
                response["message"] = 'Book Successfully Created'

                logger.info('inside post books')
                return Response(response, status=status.HTTP_201_CREATED)
            logger.error('failed post books')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,*args,**kwargs):
            id = kwargs.get("id")
            instance = Book.objects.get(id=id)
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Book Details Updation Failed"}
            serializer = self.serializer_class(data=request.data, instance=instance)
            if serializer.is_valid():
                
                serializer.save()

                response["status"]=status.HTTP_200_OK
                response["message"]="Book Updation Successfull"
                response["data"]=serializer.data

                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
            try:
                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book Removing Failed"}
                id = kwargs.get('id')
                user = Book.objects.get(id=id)
                user.delete()
                response["status"] = status.HTTP_200_OK
            
                response["message"] = 'Book Removed Successfully'
                return Response(response, status=status.HTTP_200_OK)
            except Exception:
                return Response(response, status= status.HTTP_400_BAD_REQUEST)

""" Registration """
class UserRegistrationView(APIView):
    
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "User Fetching Failed"}
            user_list = User.objects.all()
            serializer = self.serializer_class(user_list, many=True)
            response["status"] = status.HTTP_201_CREATED
            response["data"] = serializer.data
            response["message"] = 'Users Fetched Successfully'
            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Registration Failed"}
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                response["status"] = status.HTTP_201_CREATED
                response["data"] = serializer.data
                response["message"] = 'Registration Successfull'
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            instance = User.objects.get(id=id)
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"User Details Updation Failed"}
            serializer = self.serializer_class(data=request.data, instance=instance)
            if serializer.is_valid():
                
                name = serializer.validated_data.get("username")
                email = serializer.validated_data.get("email")
                password = serializer.validated_data.get("password")
            
                instance.username = name
                instance.email = email
                instance.set_password(password)
                
                instance.save()
                response["status"]=status.HTTP_200_OK
                response["message"]="Updation Successfull"
                response["data"]=serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    
                
    def delete(self,request,*args,**kwargs):
        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "User Removing Failed"}
            id = kwargs.get('id')
            user = User.objects.get(id=id)
            user.delete()
            response["status"] = status.HTTP_200_OK
          
            response["message"] = 'User Removed Successfully'
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status= status.HTTP_400_BAD_REQUEST)
        

      
""" Book Issue/Return """

class IssueBookView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Issued/Returned Details Not Found"}
            issued_list = IssueBook.objects.all()
            serializer = self.serializer_class(issued_list, many=True)

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Issued/Returned Details Fetched Succesfully'

            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book issuance Failed"}

            """ fetch email for send mail """
            id = request.data['user']
            send_mail = User.objects.get(id=id)
            e_mail = send_mail.email

            """ fetch bookname and author """
            book_id = request.data['book']
            books = Book.objects.get(id=book_id)
            book = books.title
            author = books.author
            language = books.language

            date = request.data['issue_date']
            print(date)

            if serializer.is_valid():

                serializer.save()

                response["status"] = status.HTTP_200_OK
                response["data"] = serializer.data
                response["message"] = 'Book Issued Successfully'

                message = 'Your Book  is issued successfully...! \n\n Book Name:' f"{book} \n\n Author: {author} \n\n Language: {language} \n\n Issue date: {date}\n \n Kindly return the same in 7 days. \n \n Happy Reading..!"

                send_issue_mail.delay(e_mail, message)

                return Response(response, status=status.HTTP_200_OK)
            else:
                logger.warning("issue failed....!!!!!!")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print('Exception Occured',e)


    def put(self, request, *args, **kwargs):
        try:
    
            id = kwargs.get("id")
            print(id)
            instance = IssueBook.objects.get(id=id)
            serializer = IssueSerializer(data=request.data)

            """ fetch email for send mail """
            id = request.data['user']
            send_mail = User.objects.get(id=id)
            e_mail = send_mail.email

            """ fetch bookname and author """
            book_id = request.data['book']
            books = Book.objects.get(id=book_id)
            book = books.title
            author = books.author

            date = request.data['return_date']

            if serializer.is_valid():

                status = serializer.validated_data.get("status")

                return_date = serializer.validated_data.get("return_date")

                instance.status = status

                instance.return_date = return_date

                instance.save()

                message = 'You have returned the Book..! \n\n Book Name:'  f"{book} \n\n Author: {author} \n\n Book Return Date: {date}. \n \n Thank you.!"

                send_return_mail.delay(e_mail, message)
                
                return Response({'Book Returned Successfully'})
            else:
                return Response({'Book Return Failed'} )

        except Exception as e:
            print('\n Exception Occured',e)

      
"""Fetch Issue/Return Book Details """ 

class BookDetails(APIView):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        
            try:
                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book Details Not Found"}
                id = kwargs.get('id')
                issued_list = IssueBook.objects.get(id = id)
                date = issued_list.issue_date.strftime("%d-%m-%Y")
                print(date)

                serializer = self.serializer_class(issued_list)
                
                response["status"] = status.HTTP_200_OK
                response["data"] = serializer.data
                response["message"] = 'Book Details Fetched Succesfully'

                logger.info('inside issue book details')
                return Response(response, status=status.HTTP_200_OK)
            except Exception:
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

    


""" Search """

class SearchView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Book not available"}

            name = request.data['name']
            book_obj = Book.objects.filter(title__icontains = name)
            # print(instance)
            book_list = []
            for books in book_obj:
                book = books.title
            
                book_list.append(book)
                
                response["status"] = status.HTTP_200_OK
                response["data"] = book_list
                response["message"] = 'Book is Available'
            print(book_list)
            logger.info(book_list)
            return Response(response)
            
                # else:
                #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
             print('Exception Occured',e)
            

class FilterView(APIView):

    def post(self, request):

        try:
            response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Data Fetching Failed"}

            from_date = request.data['from']
            to_date = request.data['to']
            data = IssueBook.objects.filter(issue_date__range=[from_date,to_date])
            # print(instance)
            data_list = []
            for dates in data:
                title = dates.book.title
                user = dates.user.username
            
                data_list.append(title)
                data_list.append(user)
                
                # data_set = dict(data_list)
                
              
            print(data_list)

            response["status"] = status.HTTP_200_OK
            response["data"] = data_list
            response["message"] = 'Data Fetched Successfully'
            return Response(response)


        except Exception as e:
            print('Exception Occured',e)
            logger.error(e)

        

