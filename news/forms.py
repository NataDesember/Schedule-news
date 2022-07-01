from smtplib import SMTPDataError

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm, CharField
from django.template.loader import render_to_string

from .models import Post

from django import forms

from allauth.account.forms import SignupForm, BaseSignupForm
from django.contrib.auth.models import Group

from .tasks import send_note

class PostForm(ModelForm):
    request_user = None

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categorys']

    def save(self):
        post = super(PostForm, self).save()
        user = self.request_user

        # New code: push task in queue for celery
        send_note.delay(post.id)

        # Old code was
        # for t in post.categorys.all():
        #     for s in t.subscribers.all():
        #         if s.email == user.email:
        #             html_content = render_to_string(
        #                 'post_notified.html',
        #                 {
        #                     'first_name': user.first_name,
        #                     'last_name': user.last_name,
        #                     'category': t,
        #                     'post': post,
        #                 }
        #             )
        #
        #             msg = EmailMultiAlternatives(
        #                 subject=f'Новая статья {{ t }}',
        #                 body=f'Здравствуй, {{ first_name }} {{ last_name }}. Новая статья в твоём любимом разделе {{ category }}! {{ post.title }} <br/> {{ post.text }}',
        #                 from_email='green-malahit@yandex.ru',
        #                 to=[user.email],
        #             )
        #             msg.attach_alternative(html_content, "text/html")  # добавляем html
        #             msg.send()  # отсылаем

        return post


class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categorys']


class BaseRegisterForm(SignupForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ["username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", ]

    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        html_content = render_to_string(
            'user_registered.html',
            {
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
        )

        try:
            msg = EmailMultiAlternatives(
                subject=f'Registration',
                body='Thank you for registration',
                from_email='green-malahit@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем
        except SMTPDataError:
            pass

        return user
