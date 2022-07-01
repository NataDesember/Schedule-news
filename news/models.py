from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import ForeignKey


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True)
    email = models.CharField(blank=True, max_length=256)
    rating_user = models.IntegerField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    def update_rating(self, ):
        r_post = sum([d['rating_post'] for d in Post.objects.filter(author=self).values('rating_post')]) * 3

        r_comnt = sum([d['comment_rating'] for d in Comment.objects.filter(user=self.user).values('comment_rating')])
        r_add = sum([d['comment_rating'] for d in Comment.objects.filter(post__author=self).values('comment_rating')])

        self.rating_user = r_post + r_comnt + r_add

        self.complete = True
        self.save()


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=100)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating_post = models.IntegerField(blank=True, default=0, editable=False)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f"/news/{self.id}"

    class PostChoice(models.TextChoices):
        ARTICLE = 'AR', 'Статья',
        NEWS = 'NW', 'Новость'

    field_choices = models.CharField(
        max_length=2,
        choices=PostChoice.choices,
        default=PostChoice.NEWS
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categorys = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.complete = True
        self.save()
        return self.rating_post

    def dislike(self):
        self.rating_post -= 1
        self.complete = True
        self.save()
        return self.rating_post

    def preview(self):
        return self.text[0:123].join('...')

    def __str__(self):
        return f'{self.title} {self.time_in} {self.text}'


class PostCategory(models.Model):
    post: ForeignKey = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user: ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(blank=True, default=0, editable=False)

    def like(self):
        self.comment_rating += 1
        self.complete = True
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1
        self.complete = True
        self.save()
        return self.comment_rating


