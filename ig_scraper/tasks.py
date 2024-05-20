from celery import shared_task
from .models import Influencer
import logging
from .scraper import fetch_influencer_data

logger = logging.getLogger(__name__)

@shared_task
def fetch_all_influencers_data():
    influencers = Influencer.objects.all()
    for i in influencers:
        fetch_influencer_data(i.username)
    return True