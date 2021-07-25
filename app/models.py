from django.db import models


class XlsxFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    file = models.FileField(null=True, upload_to='documents/')
    task_id = models.UUIDField(null=True)
