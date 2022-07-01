from django.contrib.auth.models import User
from news.models import *


user1 = User.objects.create_user('user_1')
user2 = User.objects.create_user('user_2')

author1 = Author.objects.create(full_name='Jo Biden', age=80, email='biden@whitehouse.gov', rating_user=0, user=user1)
author2 = Author.objects.create(full_name='Elon Musk', age=50, email='elon@spacex.com', rating_user=0, user=user2)
tema1 = Category.objects.create(category_name='Политика')
tema2 = Category.objects.create(category_name='Спорт')
tema3 = Category.objects.create(category_name='Наука')
tema4 = Category.objects.create(category_name='Космос')

article1 = Post.objects.create(title='SpaceX', text='Two of the firms Falcon 9 rockets', rating_post=0, author=author2)
article2 = Post.objects.create(title='New SpaceX', text='After the launches, Musk tweeted that his aim is to re-launch', rating_post=0, author=author2)
news1 = Post.objects.create(title='Джо Байден', text='Байден подписал новый указ', rating_post=0, author=author1)

category1=Category.objects.create(category_name='Статья')
category2=Category.objects.create(category_name='Новость')

article1.categorys.add(tema1)
article2.categorys.add(tema2)
news1.categorys.add(tema3)

comment1=Comment.objects.create(post=article1, user=user1, comment_text='Церковь не одобряет полеты в космос!', comment_rating=0)
comment2=Comment.objects.create(post=article1, user=user2, comment_text='Для чего нам нужен космос', comment_rating=0)
comment3=Comment.objects.create(post=article2, user=user1, comment_text='Эта статья не содержит полезной информации', comment_rating=0)
comment4=Comment.objects.create(post=news1, user=user2, comment_text='Это недопустимо', comment_rating=0)

comment4.like()
comment4.like()
comment4.like()
comment4.like()
comment4.like()

comment3.like()
comment3.like()
comment3.like()

comment2.like()
comment2.like()
comment2.like()

comment1.like()
comment1.like()
comment1.like()
comment1.like()
comment1.dislike()

article1.like()
article1.like()
article1.like()
article1.like()

article2.like()
article2.like()
article2.like()
article2.like()
article2.like()
article2.like()
article2.dislike()

news1.like()
news1.like()
news1.like()
news1.like()
news1.like()
news1.like()
news1.like()
news1.like()
news1.dislike()
news1.dislike()
news1.dislike()
news1.dislike()

author1.update_rating()
author2.update_rating()

print ( Author.objects.all().order_by('-rating_user')[0].full_name, Author.objects.all().order_by('-rating_user')[0].rating_user)

print (  Post.objects.all().order_by('-rating_post')[0].time_in, Post.objects.all().order_by('-rating_post')[0].author.full_name, Post.objects.all().order_by('-rating_post')[0].rating_post, Post.objects.all().order_by('-rating_post')[0].title, Post.objects.all().order_by('-rating_post')[0].preview())

article_to_print = Post.objects.all().order_by('-rating_post')[0]
for d in Comment.objects.filter(post=article_to_print):
    print (d.time_in, d.user, d.comment_rating, d.comment_text)
