from django.test import TestCase
from django.contrib.auth.models import User
from .models import Song, Voter
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class IndexViewTestCase(TestCase):
    def setUp(self):
        self.song = Song.objects.create(
            name = 'Test song',
            artist = 'Test artist',
            votes = 5,
            cover = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            is_published = True
        )

    
    def test_index_view_with_songs(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating/index.html')
        self.assertContains(response, 'Test song')
        self.assertContains(response, 'Test artist')

    
    def test_index_view_without_songs(self):
        Song.objects.all().delete()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating/index.html')
        self.assertContains(response, 'There is no songs')


class AddNewSongViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    
    def test_add_new_song_without_login(self):
        response = self.client.get('/add_song/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'rating/add_song.html')

    
    def test_add_new_song_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/add_song/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating/add_song.html')


class VoteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.song = Song.objects.create(
            name='Test song',
            artist='Test artist',
            cover = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            votes=5,
            is_published=True
        )
    

    def test_vote_view_without_login(self):
        response = self.client.get('/vote/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'rating/vote.html')
    

    def test_vote_view_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/vote/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating/vote.html')