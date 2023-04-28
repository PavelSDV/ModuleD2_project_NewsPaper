from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime

# from django.contrib.auth.forms import UserCreationForm
# from django import forms

# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    subscribers = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass
    def get_category(self):
        return self.name
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices = CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    # postCategory = models.ManyToManyField('Category', through='PostCategory')
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def email_preview(self):
        return f'{self.text[0:49]}...'

    def get_absolute_url(self):
        return f'/news/ {self.id}'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.postThrough.title + ' ' + self.categoryThrough.name

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentPost.author.authorUser.username

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()



