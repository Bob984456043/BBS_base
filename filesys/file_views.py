import os

from django.http import  HttpResponse
from rest_framework import views

from BBS_base.settings import BASE_DIR
from . import models, filesys_serializer
from rest_framework.response import Response
# Create your views here.
from rest_framework.pagination import PageNumberPagination


class SelfPaginations(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 20


class FileQureyAPI(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ret = {}
        user_id = request.query_params.get('id')
        category = request.query_params.get('category')
        if user_id != None and category == None:
            file_list = models.File.objects.filter(user_id=user_id)
        elif user_id != None and category != None:
            file_list = models.File.objects.filter(user_id=user_id, category=category)
        elif user_id == None and category != None:
            file_list = models.File.objects.filter(category=category)
        elif user_id == None and category == None:
            file_list = models.File.objects.all()

        paginate = SelfPaginations()
        page_list = paginate.paginate_queryset(file_list, request)
        f_serializer = filesys_serializer.FileSerializer(page_list, many=True)

        ret['list'] = f_serializer.data
        ret['total'] = len(file_list)
        return Response(ret)


class FileDetailAPI(views.APIView):

    def dispatch(self, request, *args, **kwargs):
        # 实现特定method执行token认证
        if request.method.lower() == 'get':
            self.authentication_classes = []
            self.permission_classes = []
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def get(self, request, *args, **kwargs):
        ret = {}
        id = request.query_params.get('id')
        file = models.File.objects.get(id=id)
        file.downloads += 1
        file.save()
        f, n = os.path.splitext(file.filename)  # 获取文件后缀名
        tmp = open(file.filepath, 'rb')

        if file.filename.endswith('.txt'):
            return HttpResponse(tmp)
        elif file.filename.endswith('.pdf'):
            return HttpResponse(tmp, content_type='application/pdf')
        elif file.filename.endswith('.jpg'):
            return HttpResponse(tmp, content_type='application / x - jpg')
        elif file.filename.endswith('.jpeg'):
            return HttpResponse(tmp, content_type='image / jpeg')
        elif file.filename.endswith('.doc') or file.filename.endswith('.docx'):
            return HttpResponse(tmp, content_type='application/msword')
        else:
            ret['msg'] = '只支持.txt,pdf,jpg,jpeg,doc,docx格式！'
            return Response(ret)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        category = request.data.get('category')
        filebrief = request.data.get('filebrief')
        post_time = request.data.get('post_time')
        if request.FILES:
            file_obj = request.FILES.get("file")
            if not file_obj:
                filename = 'none'
            else:
                filename = file_obj.name
            # post_time = request.data.get('post_time')
            filepath = os.path.join(BASE_DIR, "static", "file", filename).replace("\\", "/")
            with open(filepath, 'wb')as f:
                for i in file_obj.chunks():
                    f.write(i)
            filesize = int(file_obj.size)

        createfile = models.File.objects.create(filename=filename, category=category, filebrief=filebrief,
                                                post_time=post_time, filesize=filesize, user_id=user_id,
                                                filepath=filepath)

        return Response(filesys_serializer.FileSerializer(createfile).data)

    def delete(self, request, *args, **kwargs):
        ret = {}
        id = request.query_params.get('id')
        try:
            file = models.File.objects.get(id=id)
            os.remove(os.path.join(BASE_DIR, "static", "file", file.filename).replace("\\", "/"))
            models.File.objects.get(id=id).delete()
            ret['msg'] = '删除文件%s成功' % id
        except:
            ret['msg'] = '文件不存在'
        return Response(ret)

        # except:
        #     ret['msg']='文章不存在'
        #     return Response(ret)
