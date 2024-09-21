import redis
import requests
from django.conf import settings

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def get_gold_price():
    gold_price = redis_instance.get('gold_price')
    if gold_price is None:
        response = requests.get('https://api.metalpriceapi.com/v1/latest?access_key=YOUR_API_KEY')
        gold_price = response.json().get('rates', {}).get('XAU')
        redis_instance.set('gold_price', gold_price, ex=300)  # Cache for 5 minutes
    return float(gold_price)
