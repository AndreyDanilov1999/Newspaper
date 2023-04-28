from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news import settings
import datetime
from .models import Category, Subscriber


@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        cc='',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_message():
    for category in Category.objects.all():
        mailing_list = list(
            Subscriber.objects.filter(
                category=category
            ).values_list(
                'user__username',
                'user__email',
                'category__name'
            )
        )
        posts_list = list(category.post_set.filter(
                dateCreation__gt=datetime.datetime.now() - datetime.timedelta(days=7)
            ))
        if len(mailing_list) > 0 and len(posts_list) > 0:
            for user, email, category_name in mailing_list:

                html_content = render_to_string(
                    'weekly_posts.html',
                    {
                        'link': settings.SITE_URL,
                        'name': user,
                        'category': category,
                        'posts': posts_list,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject='Сводка новостей за прошедшую неделю',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
