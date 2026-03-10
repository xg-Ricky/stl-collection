from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from image_upload.models import Entry


class GalleryFilterTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='gallery-user',
			password='test-password-123'
		)
		self.client.force_login(self.user)

		Entry.objects.create(name='Alpha One', publisher='Publisher A', range='Range A1')
		Entry.objects.create(name='Alpha Two', publisher='Publisher A', range='Range A2')
		Entry.objects.create(name='Beta One', publisher='Publisher B', range='Range B1')

	def test_gallery_ranges_are_limited_to_selected_publisher(self):
		response = self.client.get(reverse('collection:gallery'), {'publisher': 'Publisher A'})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['ranges']), ['Range A1', 'Range A2'])

	def test_gallery_clears_stale_range_when_publisher_changes(self):
		response = self.client.get(
			reverse('collection:gallery'),
			{
				'publisher': 'Publisher B',
				'range': 'Range A1',
			}
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['range_filter'], '')
		self.assertEqual(list(response.context['ranges']), ['Range B1'])
		self.assertEqual(response.context['query_string'], 'publisher=Publisher+B')
		self.assertEqual(response.context['page_obj'].paginator.count, 1)
		self.assertEqual(response.context['page_obj'].object_list[0].publisher, 'Publisher B')
