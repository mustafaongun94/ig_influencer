import os
import instaloader
import boto3
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

def download_image_to_s3(img_url, bucket_name, s3_path):
    try:
        img_data = requests.get(img_url).content
        s3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=img_data)
        s3_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_path}"
        print(f"Image successfully uploaded to {s3_url}")
        return s3_url
    except Exception as e:
        print(f"Failed to upload image to S3: {e}")
        return None

def fetch_influencer_data(username):
    try:
        time.sleep(15)
        L = instaloader.Instaloader()

        L.login(ig_username, password)

        profile = instaloader.Profile.from_username(L.context, username)

        influencer, created = Influencer.objects.update_or_create(
            username=username,
            defaults={'full_name': profile.full_name}
        )

        posts = profile.get_posts()
        for post in posts:
            s3_path = f"influencers/{username}/posts/{post.shortcode}.jpg"
            media_url = download_image_to_s3(post.url, settings.AWS_STORAGE_BUCKET_NAME, s3_path)
            
            Post.objects.update_or_create(
                post_id=post.shortcode,
                defaults={
                    'influencer': influencer,
                    'caption': post.caption,
                    'media_url': media_url,
                    'like_count': post.likes,
                    'comment_count': post.comments,
                    'created_at': datetime.fromtimestamp(post.date_utc.timestamp())
                }
            )

        stories = L.get_stories(userids=[profile.userid])
        for story in stories:
            items = story.get_items()
            for item in items:
                s3_path = f"influencers/{username}/stories/{item.mediaid}.jpg"
                media_url = download_image_to_s3(item.url, settings.AWS_STORAGE_BUCKET_NAME, s3_path)
                
                Story.objects.update_or_create(
                    story_id=item.mediaid,
                    defaults={
                        'influencer': influencer,
                        'media_url': media_url,
                        'created_at': datetime.fromtimestamp(item.date_utc.timestamp())
                    }
                )
    except Exception as e:
        print(str(e))
        return False

