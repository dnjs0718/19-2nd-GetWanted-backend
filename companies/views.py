import json

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator
from django.db.models      import Q
from django.db             import connection
from django.shortcuts      import get_object_or_404

from .models               import Notification, Tag, Like
from users.utils           import login_required
from .upload               import excel_export

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, permissions, serializers

import xlwt

from django.http import HttpResponse

from .models import Company


class NotificationSerializer(serializers.Serializer):
    tag = serializers.IntegerField(help_text="태그 필터링", required=False)
    page = serializers.IntegerField(help_text="페이지", default=1, required=False)
    search = serializers.CharField(help_text="검색어", required=False)


class NotificationView(APIView):
    @swagger_auto_schema(query_serializer=NotificationSerializer)
    def get(self,request):
        try:
            tag              = request.GET.get('tag')
            page             = request.GET.get('page',1)
            search           = request.GET.get('search')

            q = Q()

            if search:
                q &= (Q(title__icontains=search) | Q(company__name__icontains=search))

            if tag:
                get_object_or_404(Tag,id=tag)
                q &= Q(tag__id=tag)
            
            notification_zip = Notification.objects.select_related('company').prefetch_related('image_set','like_set').filter(q)

            paginator        = Paginator(notification_zip,16)
            notifications    = paginator.get_page(page)

            notification_list = [{
                'title'      : notification.title,
                'image'      : notification.image_set.first().image_url,
                'id'         : notification.id,
                'area'       : notification.company.address.split()[0],
                'company'    : notification.company.name,
                'like_count' : notification.like_set.filter(is_liked=1).count()
                } for notification in notifications]

            return JsonResponse({'notification_list' : notification_list, 'page' : paginator.num_pages}, status = 200)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'},status = 400)

            
class TagView(APIView):
    """
        태그를 나타내는 API

        ---
        # 내용
            - id : PK 값
            - name : 태그 이름
    """
    def get(self,request):
        tags = Tag.objects.all()
        tag_list =[{
            'id'   : tag.id,
            'name' : tag.name
        } for tag in tags]

        return JsonResponse({'tag_list': tag_list}, status=200)


class DetailSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField(help_text='공고 PK', required=True)

class NotificationDetailView(APIView):
    @swagger_auto_schema(path_serializer=DetailSerializer)
    def get(self,request,notification_id):
        try:
            notification    = Notification.objects.select_related('company').prefetch_related('image_set','tag').get(id=notification_id)
            notification_detail = [{
                'notification_id' : notification.id,
                'title'           : notification.title,
                'description'     : notification.description,
                'image_list'      : [{'id'        : image.id,
                                      'image_url' : image.image_url
                                     } for image in notification.image_set.all()],
                'tag_list'        : [{'id'   : tag.id,
                                      'name' : tag.name
                                     } for tag in notification.tag.all()],
                'company_name'    : notification.company.name,
                'company_address' : notification.company.address,
                'company_area'    : notification.company.address.split()[0],
                'latitude'        : notification.company.latitude,
                'longitude'       : notification.company.longitude 
                }]
                
            return JsonResponse({'NOTIFICATION_DETAIL' : notification_detail}, status=200)

        except Notification.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NOTIFICATION_DOES_NOT_EXIST'},status=404)

class ContactForm(serializers.Serializer):
    notification = serializers.IntegerField()

class NotificationLikeView(APIView):
    @swagger_auto_schema(request_body=ContactForm)
    @login_required
    def post(self,request):
        try:
            data             = json.loads(request.body)
            notification     = Notification.objects.get(id=data['notification'])
            user             = request.user
            liked            = Like.objects.select_related('notification','user').filter(
                                user=user,
                                notification=notification,
                                is_liked=1)
            unliked          = Like.objects.select_related('notification','user').filter(
                                user=user, 
                                notification=notification, 
                                is_liked=0)

            if liked.exists():
                liked.update(is_liked=0)

                return JsonResponse({'MESSAGE': 'UNLIKED',
                                     'LIKE_COUNT': notification.like_set.filter(is_liked=1).count()}, 
                                     status=201)
            
            if unliked.exists():
                unliked.update(is_liked=1)

                return JsonResponse({'MESSAGE': 'LIKED',
                                     'LIKE_COUNT': notification.like_set.filter(is_liked=1).count()}, 
                                     status=201)

            else:
                Like.objects.create(user=user, notification=notification, is_liked=1)

                return JsonResponse({'MESSAGE': 'LIKED',
                                     'LIKE_COUNT': notification.like_set.filter(is_liked=1).count()},
                                      status=201)

        except Notification.DoesNotExist:
            return JsonResponse({"MESSAGE": "NOTIFICATION_DOES_NOT_EXIST"}, status=404)
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE': "VALUE_ERROR"}, status = 400)


    def excel_export(request):
            response = HttpResponse(content_type= "application/vns.ms-excel")
            response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
            wb = xlwt.Workbook(encoding='ansi')
            ws = wb.add_sheet('테스트테스트카이트')

            row_num = 0
            col_names = ['name', 'address']

            for idx, col_name in enumerate(col_names):
                ws.write(row_num, idx, col_name)

            rows = Company.objects.all().values_list('name','address')

            for row in rows:
                row_num+=1
                for col_num, attr in enumerate(row):
                    ws.write(row_num, col_num, attr)
            
            wb.save(response)
            return response
