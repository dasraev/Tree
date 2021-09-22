from dreeapp.models import MostPlanted
from instagramy import InstagramUser
from datetime import datetime
from urllib.request import urlretrieve
from requests_html import HTMLSession

username = 'rasulovmuxtor'
password = 'Parol123'

import os
from django.conf import settings


def get_sessionid():
    session = HTMLSession()
    url = 'https://www.instagram.com/accounts/login/'
    r = session.get(url)
    csrftoken = r.cookies.get('csrftoken')

    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    time = int(datetime.now().timestamp())
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    response = session.post(login_url, data=payload,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                                "X-Requested-With": "XMLHttpRequest",
                                "Referer": "https://www.instagram.com/accounts/login/",
                                "x-csrftoken": csrftoken
                            }
                            )
    if response.status_code == 200:
        sessionid = response.cookies.get('sessionid')
        return sessionid


def get_feed(username=None,type=None,account_link=None,tree_amount=None):
    sessionid = get_sessionid()
    if not sessionid:
        return "Password or login is incorrect!"
    if not username:
        username = 'instagram'
        # username = \
        #     getattr(Settings.objects.last(), 'instagram', 'https://www.instagram.com/haval.uzbekistan/').split('/')[3]
    user = InstagramUser(username, sessionid=sessionid)

    user_model, created = MostPlanted.objects.get_or_create(username=username,
                                                                 defaults={'name': user.fullname})
    profile_picture_path = f'instagram/{username}.jpg'
    urlretrieve(user.profile_picture_url,
                filename=os.path.join(settings.MEDIA_ROOT, profile_picture_path))
    user_model.image.name = profile_picture_path
    user_model.type=type
    user_model.account_link=account_link
    if isinstance(user_model.tree_amount,int):
        user_model.tree_amount+=tree_amount
    else:
        user_model.tree_amount=tree_amount

    user_model.save()
    # data = user.user_data
    # post_list = data['edge_owner_to_timeline_media']['edges']
    # post_list.reverse()
    # for post in post_list:
    #     thumbnail_url = post['node']['thumbnail_src']
    #     for thumbnail in post['node']['thumbnail_resources']:
    #         if thumbnail['config_width'] > 212:
    #             thumbnail_url = thumbnail['src']
    #             break
    #
    #     # display_ur'=post['node']['display_url'],
    #     # shortcode=post['node']['shortcode'],
    #     # preview_like_count= post['node']['edge_media_preview_like']['count'],
    #     defaults = {
    #         'comments_count': post['node']['edge_media_to_comment']['count'],
    #         'likes_count': post['node']['edge_liked_by']['count'],
    #         'shortcode': post['node']['shortcode'],
    #     }
    #     post, created = InstagramFeed.objects.update_or_create(
    #         identifier=post['node']['id'], defaults=defaults
    #     )
    #     feed_picture_path = f'instagram/feed/{post.identifier}.jpg'
    #     urlretrieve(thumbnail_url,
    #                 filename=os.path.join(settings.MEDIA_ROOT, feed_picture_path))
    #     post.thumbnail.name = feed_picture_path
    #     post.save()
