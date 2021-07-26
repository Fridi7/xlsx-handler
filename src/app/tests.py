from io import BytesIO

import openpyxl
from django.urls import reverse
from rest_framework.test import APITestCase

from app.utils import token_sign


class AddTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        workbook = openpyxl.Workbook()
        worksheet = workbook.create_sheet('test')
        worksheet.append(['test', 'before', 'after'])
        worksheet.insert_rows(1)
        worksheet.append(['test', '1, 2, 4, 7', '4, 7, 1, '])

        data = BytesIO()
        workbook.save(data)
        cls.files = {'file': ('test.xlsx', data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

    def test_auth(self):
        url = reverse('get_token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.json()['token'], token_sign())

    def testNoError(self):
        self.skipTest('WIP')
        url = reverse('upload')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_sign()}')

        response = self.client.post(url, files=self.files)
        self.assertEqual(response.status_code, 200)

        self.assertIn('task_id', response.json())
