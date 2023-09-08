from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.http import HttpResponse

from .models import User


class PostTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = User.objects.create_superuser("superuser")
        cls.authorized_user1 = User.objects.create_user("authorized1")
        cls.authorized_user2 = User.objects.create_user("authorized2")
        cls.unauthorized_user = User.objects.create_user("unauthorized")
        cls.post_data = {
            "title": "test title",
            "body": "test body",
            "owner": cls.authorized_user1,
        }

        cls.follow_data = {"follower": cls.authorized_user1, "following": cls.superuser}

    # 전체 사용자 목록에서 자신을 제외한 목록이 잘 나오는지 테스트
    def test_user_list_without_self(self):
        self.client.force_login(self.authorized_user1)
        res: HttpResponse = self.client.get("/users/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.authorized_user1, res.data)

    # 본인의 게시물만 수정, 삭제가 가능한지 테스트
    # follow / unfollow 기능이 잘 작동하는지 테스트
    # follow한 사람들이 올린 게시물을 잘 확인할 수 있는지 테스트
