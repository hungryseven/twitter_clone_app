import re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import CICharField

from authorization.models import CustomUser
from utils.funcs import build_url

# Create your models here.

User = settings.AUTH_USER_MODEL

def filter_tweet_text(text):
    '''
    Фильтрует текст твита и возвращает список с валидными
    именами пользователей и тегами без повторений.
    '''
    filtered = []

    # Для тегов(левая часть):
    # (^|\B) - соответствует либо началу строки, либо тому,
    # что слева не граница слова, т.е. слева не буквы.
    # # - соответствует совпадению с символом "#".
    # (?![0-9_]+\b) - negative lookahead.
    # За символом "#" не могут быть символы [0-9_] от 1 до
    # неограниченного количества, если они являются границей слова.
    # ([a-zA-Zа-яА-ЯёЁ0-9_]+) - соответствует от 1 до неограниченного количества символов.
    # (\b|\r) - соответствует границе слова справа, т.е. справа пусто или не буква.

    # Для юзернеймов(правая часть):
    # (?<!\S) - соответствует тому, что слева от символа "@"
    # может быть только пробел.
    # @ - соответствует совпадению с символом "@".
    # (\w{4,15})\b - соответствует от 4 до 15 символов [a-zA-Z0-9_] с границей.
    # (?!.*@) - соответствует тому, что после юзернейма может идти любое количество
    # символов, кроме "@".
    pattern = r'((^|\B)#(?![0-9_]+\b)([a-zA-Zа-яА-ЯёЁ0-9_]+)(\b|\r))|((?<!\S)@(\w{4,15})\b(?!.*@))'
    for word in text.split():
        if '@' in word or '#' in word:
            match = re.search(pattern, word)
            if match and match.group() not in filtered:
                filtered.append(match.group())
    return filtered

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # После сохранения объекта твита в БД фильтруем его текст
        # на наличие юзернеймов и тегов.
        filtered_text = filter_tweet_text(self.text)
        for word in filtered_text:
            # Добавляем пользователю, которой упоминается в тексте,
            # уведомление, если он существует.
            if word[0] == '@':
                try:
                    user = CustomUser.objects.get(username=word[1:])
                    user.notifications.add(self, through_defaults={'timestamp': self.pub_date})
                except CustomUser.DoesNotExist:
                    continue

            # Создаем новый тег или получаем объект тега, если он уже существует,
            # и связываем с текущим твитом.
            elif word[0] == '#':
                tag, created = Tag.objects.get_or_create(tag_name=word)
                tag.related_tweets.add(self)

    def __str__(self):
        if len(self.text) > 50:
            return self.text[:51] + '...'
        return self.text

    def get_absolute_url(self):
        return reverse('tweets:detail_tweet', kwargs={'username': self.user.username, 'pk': self.pk})

class Tag(models.Model):

    tag_name = CICharField(
        max_length=140,
        unique=True,
        verbose_name='Тег'
    )
    related_tweets = models.ManyToManyField('Tweet', blank=True, related_name='related_tags', verbose_name='Связанные твиты')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return build_url('explore:search', get={'q': self, 'f': ''})