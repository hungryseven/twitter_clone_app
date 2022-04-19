from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetRetweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(MPTTModel):
    '''
    Класс, наследющийся от класса MPTTModel, который реализован на основе MPTT алгоритма,
    и представляющий модель таблицы БД с твитами пользователей.
    Связан зависимостью с моделью CustomUser на стороне "много" и рекурсивной зависимостью с самим собой.
    '''
    text = models.CharField(max_length=140, db_index=True, verbose_name='Текст твита')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_tweets', through='TweetLike')
    retweets = models.ManyToManyField(User, blank=True, related_name='retweeted_tweets', through='TweetRetweet')
    bookmarks = models.ManyToManyField(User, blank=True, related_name='bookmarked_tweets', through='TweetBookmark')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets', verbose_name='Пользователь')
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Является ответом на твит')

    class Meta:
        verbose_name = 'твит'
        verbose_name_plural = 'Твиты'
        ordering = ('id',)

    def __str__(self):
        return self.text[:51] + '...'

    def get_absolute_url(self):
        return reverse('tweets:detail_tweet', kwargs={'username': self.user.username, 'pk': self.pk})