import string
import random
import json
import requests
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.core.mail import EmailMessage

from users.models      import User, Position, ApplyList
from users.validations import email_validation, phone_validation, password_validation
from users.utils       import login_required, social_signin
from companies.models  import Notification
from resumes.utils     import user_infomation

from my_settings       import SECRET_KEY, algorithm

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phonenumber  = data['phonenumber']
            position     = data['position']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_USER'}, status=401)

            if not email_validation(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if not password_validation(password):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)

            if not phone_validation(phonenumber):
                return JsonResponse({'MESSAGE': 'INVALID_NUMBER'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                    email       = email,
                    password    = hashed_password,
                    name        = name,
                    phonenumber = phonenumber,
                    position_id = Position.objects.get(name=position).id
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

class EmailCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']

            if not email_validation(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ACCOUNT_NOT_EXIST'}, status=401)

            if User.objects.get(email=email).is_social:
                return JsonResponse({'MESSAGE': 'USE_SOCIAL_LOGIN'}, status=400)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE': 'INCORRECT_PASSWORD'}, status=400)

            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm = algorithm)

            return JsonResponse({'MESSAGE':'SUCCESS', 'TOKEN': access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

class ApplyView(View):
    @login_required
    def get(self, request):
        try:
            user            = request.user
            notification_id = request.GET['notification']

            if not Notification.objects.filter(id=notification_id).exists():
                return JsonResponse({'MESSAGE':'INVALID_NOTIFICATION_ID'}, status=401)

            if not ApplyList.objects.filter(user_id = user.id, notification_id = notification_id).exists():
                return JsonResponse({'MESSAGE': 'SUCCESS','USER_INFORMATION' : user_infomation(user)}, status=200)

            return JsonResponse({'MESSAGE': 'ALREADY_APPLY'}, status=400)
        
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': "VALUE_ERROR"}, status=400)

    @login_required
    def post(self, request):
        data            = json.loads(request.body)
        user            = request.user
        notification_id = data['notification_id']

        ApplyList.objects.create(user_id = user.id, notification_id = notification_id)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

class ApplylistView(View):
    @login_required
    def get(self, request):
        user = request.user
        
        applylists = ApplyList.objects.filter(user_id = user.id)

        user_applylists = [
                {
                    'img'  : applylist.notification.image_set.all().first().image_url,
                    'company_name'   : applylist.notification.company.name,
                    'apply_position' : '웹 개발자',
                    'apply_date'     : applylist.created_at.strftime('%Y-%m'),
                    'apply_status'   : '접수'
                    } for applylist in applylists]

        return JsonResponse({'MESSAGE': 'SUCCESS', 'APPLYLIST' : user_applylists }, status=200)

class KakaoSignin(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            access_token       = data['Authorization']
            user_info_url      = 'https://kapi.kakao.com/v2/user/me'
            user_info_headers  = {'Authorization': 'Bearer ' + access_token}

            user_info_data = requests.get(user_info_url, headers = user_info_headers).json()

            user_name  = user_info_data['properties']['nickname']
            user_email = user_info_data['kakao_account']['email']

            social_login = social_signin(user_name, user_email)
        
            if social_login == 'INVALID_EMAIL':
                return JsonResponse({"MESSAGE": "INVALID_EMAIL"}, status=401)
        
            return JsonResponse({'MESSAGE': 'SUCCESS', 'TOKEN' : social_login }, status=201)        
        except:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

class GoogleSignin(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            id_token      = data['Authorization']
            user_info_url = 'https://oauth2.googleapis.com/tokeninfo'

            user_info_data = requests.get(user_info_url+'?id_token={}'.format(id_token)).json()

            user_name  = user_info_data['name']
            user_email = user_info_data['email']

            social_login = social_signin(user_name, user_email)

            if social_login == 'INVALID_EMAIL':
                return JsonResponse({"MESSAGE": "INVALID_EMAIL"}, status=401)

            return JsonResponse({'MESSAGE': 'SUCCESS', 'TOKEN' : social_login }, status=201)
        except:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

class NaverSignin(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            access_token  = data['Authorization']
            user_info_url = 'https://openapi.naver.com/v1/nid/me'
            headers       = { 'Authorization' : 'Bearer ' + access_token }

            user_info_data = requests.get(user_info_url, headers = headers).json()

            user_name    = user_info_data['response']['name']
            user_email   = user_info_data['response']['email']

            social_login = social_signin(user_name, user_email)

            if social_login == 'INVALID_EMAIL':
                return JsonResponse({"MESSAGE": "INVALID_EMAIL"}, status=401)

            return JsonResponse({'MESSAGE': 'SUCCESS', 'TOKEN' : social_login }, status=201)

        except:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

class ResetPassword(View):
    def patch(self, request):
        try:
            data  = json.loads(request.body)
            email = data['email']
        
            password = ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(9))

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
            email_message = EmailMessage(
                'GetWanted 비밀번호 변경', 
                '귀하의 비밀번호는 아래 문자로 변경되었습니다.\n\n{}\n\n이용해 주셔서 감사합니다.'.format(password), 
                to = [email])
        
            email_message.send()
        
            user = User.objects.get(email=email)
        
            user.password = hashed_password
            user.save()
        
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)