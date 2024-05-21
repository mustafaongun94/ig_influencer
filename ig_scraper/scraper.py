import os
import random

import instaloader
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from datetime import datetime
from .models import Influencer, Post, Story
import time
from dotenv import load_dotenv
import requests

load_dotenv()

ig_username = os.environ.get("ig_username")
password = os.environ.get("password")

s3_client = boto3.client(
    's3',
    region_name=settings.AWS_S3_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


def download_media_to_s3(media_url, bucket_name, s3_path):
    try:
        response = requests.get(media_url)
        content_type = response.headers['Content-Type']

        if 'image' in content_type:
            media_type = 'image'
        elif 'video' in content_type:
            media_type = 'video'
        else:
            print("Unsupported media type")
            return None

        s3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=response.content, ContentType=content_type)
        s3_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_path}"
        print(f"{media_type.capitalize()} successfully uploaded to {s3_url}")
        return s3_url

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"Failed to upload media to S3: {e}")
        return None

def fetch_influencer_data(username):
    try:
        L = instaloader.Instaloader()

        L.login(ig_username, password)

        profile = instaloader.Profile.from_username(L.context, username)

        influencer, created = Influencer.objects.update_or_create(
            username=username,
            defaults={'full_name': profile.full_name}
        )

        for post in profile.get_posts():
            time.sleep(5)

            if post.is_video:
                media_type = "videos"
                media_url = post.video_url
                extension = "mp4"
            else:
                media_type = "posts"
                media_url = post.url
                extension = "jpg"

            s3_path = f"influencers/{profile.username}/{media_type}/{post.shortcode}.{extension}"
            s3_media_url = download_media_to_s3(media_url, settings.AWS_STORAGE_BUCKET_NAME, s3_path)

            if post.typename == "GraphSidecar":
                for sidecar in post.get_sidecar_nodes():
                    if sidecar.is_video:
                        media_type = "videos"
                        media_url = sidecar.video_url
                        extension = "mp4"
                    else:
                        media_type = "posts"
                        media_url = sidecar.display_url
                        extension = "jpg"
                    sidecar_id = post.shortcode + str(random.randint(1,100000))+ str(random.randint(1,10000))
                    s3_path = f"influencers/{profile.username}/{media_type}/{sidecar_id}.{extension}"
                    s3_media_url = download_media_to_s3(media_url, settings.AWS_STORAGE_BUCKET_NAME, s3_path)

                    Post.objects.update_or_create(
                        post_id=sidecar_id,
                        defaults={
                            'influencer': influencer,
                            'caption': post.caption,
                            'media_url': s3_media_url,
                            'like_count': post.likes,
                            'comment_count': post.comments,
                            'created_at': datetime.fromtimestamp(post.date_utc.timestamp()),
                            'is_video': sidecar.is_video
                        }
                    )
            else:
                Post.objects.update_or_create(
                post_id=post.shortcode,
                defaults={
                    'influencer': influencer,
                    'caption': post.caption,
                    'media_url': s3_media_url,
                    'like_count': post.likes,
                    'comment_count': post.comments,
                    'created_at': datetime.fromtimestamp(post.date_utc.timestamp()),
                    'is_video': post.is_video
                }
                )
        stories = L.get_stories(userids=[profile.userid])
        for story in stories:
            time.sleep(5)
            items = story.get_items()
            for item in items:
                if item.is_video:
                    media_type = "videos"
                    media_url = item.video_url
                    extension = "mp4"
                else:
                    media_type = "stories"
                    media_url = item.url
                    extension = "jpg"

                s3_path = f"influencers/{username}/{media_type}/{item.mediaid}.{extension}"
                s3_media_url = download_media_to_s3(media_url, settings.AWS_STORAGE_BUCKET_NAME, s3_path)

                Story.objects.update_or_create(
                    story_id=item.mediaid,
                    defaults={
                        'influencer': influencer,
                        'media_url': s3_media_url,
                        'created_at': datetime.fromtimestamp(item.date_utc.timestamp()),
                        'is_video': item.is_video
                    }
                )
    except Exception as e:
        print(str(e))
        return False

