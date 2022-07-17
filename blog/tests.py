from django.test import TestCase, Client, RequestFactory
from . import models
from . import views
from django.contrib.auth.models import User


class PostTestCase(TestCase):
    def setUp(self):
        password ='123'
        self.factory = RequestFactory()
        self.user = User.objects.create_user('textcase', '', password)
        models.Post.objects.create(title= "test test", text="random test text", private="True", author=self.user)
        
    def testPostContent(self):
        post = models.Post.objects.get(title="test test")
        self.assertEqual(post.text, "random test text")

    def testDrafts(self):
        request = self.factory.get('/myposts')
        request.user = self.user
        response = views.PostDraft.as_view()(request)
        
        # client = Client()
        # client.login(username='textcase', password = '123')
        # post = models.Post.objects.get(title="test test")
        self.assertEqual(response.status_code, 200)
        