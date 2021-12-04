from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .views import home, board_topics, new_topic
from .models import Board,Topic, Post, User
from .forms import NewTopicForm

# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        self.board=Board.objects.create(name='Django', description='Django board')
        url=reverse('home')
        self.response=self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view=resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url=reverse('board_topics', kwargs={'number': 1})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    def test_home_view_status_code(self):
        url=reverse('home')
        response=self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func , home)

        
class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')

    def test_board_topics_view_success_status_code(self):
        url=reverse('board_topics', kwargs={'number': 1})
        response=self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url=reverse('board_topics', kwargs={'number': 99})
        response=self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        view=resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url=reverse('board_topics', kwargs={'number':1})
        response=self.client.get(board_topics_url)
        homepage_url=reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')
        User.objects.create_superuser(username='ali', email='ali@fada.com', password='123')

    def test_new_topics_view_success_status_code(self):
        url=reverse('new_topic', kwargs={'number': 1})
        response=self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url=reverse('new_topic', kwargs={'number': 99})
        response=self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_new_topic_url_resolves_new_topic_view(self):
        view=resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_board_topics_view_contains_navigation_links(self):
        new_topic_url=reverse('new_topic', kwargs={'number':1})
        homepage_url=reverse('home')
        board_topics_url=reverse('board_topics', kwargs={'number':1})
        response=self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_csrf(self):
        url=reverse('new_topic', kwargs={'number':1})
        response=self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_new_topic_valid_post_data(self):
        url=reverse('new_topic', kwargs={'number':1})
        data={'subject': 'Test title', 'message': 'lorem ipsum dolor sit amet'}
        response=self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url=reverse('new_topic', kwargs={'number':1})
        response=self.client.post(url, {})
        self.assertEquals(response.status_code, 302)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url=reverse('new_topic', kwargs={'number':1})
        data={ 'subject': '', 'message': ''}
        response=self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url=reverse('new_topic', kwargs={'number':1})
        response=self.client.get(url)
        form=response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        url=reverse('new_topic', kwargs={'number':1})
        response=self.client.post(url, {})
        form=response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
