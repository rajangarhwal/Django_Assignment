from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, AdvisorSerializer, BookingSerializer
from rest_framework.response import Response
from .models import User, Advisor, Booking
import jwt, datetime

# Create your views here.

class Register(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        name = request.data['name']
        if email is None or email == '':
            return Response(status = 400)
        if password is None or password == '':
            return Response(status = 400)
        if name is None or name == '':
            return Response(status = 400)

        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user = User.objects.filter(email=email).first()        

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        return Response({'JWT Authentication Token': token, 'User id':user.id}, status = 200)        



class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if email is None or email == '':
            return Response(status = 400)
        if password is None or password == '':
            return Response(status = 400)


        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status = 400)
        
        if not user.check_password(password):
            return Response(status = 401)

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        return Response({'JWT Authentication Token': token, 'User id':user.id}, status = 200)


class Admin(APIView):
    def post(self, request):
        name = request.data['name']
        photo_url = request.data['photo_url']
        if photo_url is None or photo_url == '':
            return Response(status = 400)
        if name is None or name == '':
            return Response(status = 400)

        serializer = AdvisorSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status = 200)   
    
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response(status = 400)
        else:
            datas = Advisor.objects.all()
            data_response = []
            for data in datas:
                some_1 = {
                    "Advisor_name": data.name,
                    "Advisor_Profile_pic":data.photo_url.url,
                    "Advisor_id": data.id
                }
                data_response.append(some_1)
            return Response(data_response)





class Adv(APIView):
    def post(self, request, id, a_id):
        time = request.data['time']
        user_id = id
        advisor_id = a_id

        if time is None or time == '':
            return Response(status = 400)
        user = User.objects.filter(id=user_id).first()
        advisor = Advisor.objects.filter(id = advisor_id).first()

       

        if user is None:
            return Response(status = 400)
        if advisor is None:
            return Response(status = 400)
        
        checkdata = Booking.objects.all()
        for me in checkdata:
            if me.advisor_id == advisor_id and me.time == time:
                    return Response(status = 400)


        dt = {
            "time": time,
            "user_id":user_id,
            "advisor_id":advisor_id
        }

        serializer = BookingSerializer(data = dt)
        serializer.is_valid(raise_exception = True)
        serializer.save()
       
        return Response(status = 200)      

class ADVBooking(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()

        if user is None:
            return Response(status = 400)

        datas = Booking.objects.all()
        data_response = []
        for data in datas:
            if data.user_id == id:
                advisor_id = data.advisor_id
                book = Advisor.objects.filter(id = advisor_id).first()
                some_1 = {
                    "Advisor_name": book.name,
                    "Advisor_Profile_pic":book.photo_url.url,
                    "Advisor_id": book.id,
                    "Booking_time": data.time,
                    "Booking_id": data.id,
                }
                data_response.append(some_1)
        return Response(data_response, status = 200)
       

