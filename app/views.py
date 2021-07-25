from celery import states
from celery.result import AsyncResult
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from app import utils
from app.models import XlsxFile
from app.tasks import xlsx_processing
from xlsx_handler.settings import AVAILABLE_FILE_EXTENSIONS, MAX_UPLOAD_SIZE


@api_view(['GET'])
def get_token(request):
    return Response({'token': utils.token_sign()})


@api_view(['POST'])
@authentication_classes([utils.CustomTokenAuthentication])
def upload(request):
    if "file" not in request.FILES:
        return Response("Upload xlsx file", status=HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    if file.size > MAX_UPLOAD_SIZE:
        return Response("Imported file is too large", HTTP_400_BAD_REQUEST)

    if file.content_type not in AVAILABLE_FILE_EXTENSIONS:
        return Response("Upload xlsx file", status=HTTP_400_BAD_REQUEST)

    instance = XlsxFile.objects.create(file=file, name=file.name)

    task = xlsx_processing.delay(instance.id)
    instance.task_id = task.id
    instance.save(update_fields=['task_id'])

    return Response({'task_id': task.id})


@api_view(['GET'])
@authentication_classes([utils.CustomTokenAuthentication])
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    instance = XlsxFile.objects.get(task_id=task_id)
    result = {
        'task_id': task_id,
        'date_upload': instance.uploaded_at.replace(tzinfo=None),
        'date_done': task_result.date_done,
        'task_status': 'UPLOADED' if task_result.status == states.PENDING else task_result.status,
        'task_result': task_result.result
    }
    return Response(result)
