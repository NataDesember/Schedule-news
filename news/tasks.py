from celery import shared_task
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


# crontab task, every monday 8.00AM
@shared_task
def send_notifications():
    N_DAYS_AGO = 7

    today = datetime.now()
    n_days_ago = today - datetime.timedelta(days=N_DAYS_AGO)
    for article in Post.objects().filter(time_in__gt=n_days_ago).order_by("-time_in"):
        send_note.delay(article.id)


# Task from UI every time Post have created
@shared_task
def send_note(post_id):
    article = Post.objects.get(post_id)
    for t in article.categorys.all():
        for s in t.subscribers.all():
            html_content = render_to_string(
                'scheduler_job.html',
                {
                    'category': t,
                    'post': article,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новая статья {{ t }}',
                body=f'Здравствуй, {{ s.first_name }} {{ s.last_name }}. Новая статья в твоём любимом разделе {{ category }}! {{ post.title }} <br/> {{ post.text }}',
                from_email='green-malahit@yandex.ru',
                to=[s.email],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем

