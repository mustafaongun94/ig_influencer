from django.test import TestCase, Client
from django.urls import reverse
from .models import Influencer, Post, Story
from .forms import InfluencerForm
from unittest.mock import patch
from datetime import datetime

class InfluencerViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.influencer1 = Influencer.objects.create(username="testuser1")
        self.influencer2 = Influencer.objects.create(username="testuser2")
        self.post1 = Post.objects.create(influencer=self.influencer1, caption="Post content 1",like_count=10,comment_count=1,created_at=datetime.now())
        self.story1 = Story.objects.create(influencer=self.influencer1, created_at = datetime.now())

    def test_influencer_list_view(self):
        response = self.client.get(reverse('influencer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'influencer/influencer_list.html')
        self.assertContains(response, self.influencer1.username)
        self.assertContains(response, self.influencer2.username)

    def test_influencer_detail_view(self):
        response = self.client.get(reverse('influencer_detail', args=[self.influencer1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'influencer/influencer_detail.html')
        self.assertContains(response, self.influencer1.username)
        self.assertContains(response, self.post1.caption)
        self.assertContains(response, self.story1)

    def test_influencer_add_view_get(self):
        response = self.client.get(reverse('influencer_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'influencer/influencer_form.html')
        self.assertIsInstance(response.context['form'], InfluencerForm)

    @patch('ig_scraper.views.fetch_influencer_data')
    def test_influencer_add_view_post(self, mock_fetch):
        response = self.client.post(reverse('influencer_add'), {'username': 'newuser'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Influencer.objects.filter(username='newuser').exists())
        mock_fetch.assert_called_once_with('newuser')

    def test_influencer_delete_view_get(self):
        response = self.client.get(reverse('influencer_delete', args=[self.influencer1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'influencer/influencer_confirm_delete.html')

    def test_influencer_delete_view_post(self):
        response = self.client.post(reverse('influencer_delete', args=[self.influencer1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Influencer.objects.filter(pk=self.influencer1.pk).exists())