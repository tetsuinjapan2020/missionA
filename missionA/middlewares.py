import time
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse
from django.core.cache import caches

MAX_REQUEST_PER_MINIUTE = 60
PERIOD = 60

class LimitRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR")
        now = time.time()
        cache = caches['default']
        requests = cache.get(ip,[])
        while requests and time.time() -  requests[-1] > PERIOD:
            requests.pop()
        requests.insert(0, time.time())
        cache.set(ip, requests, timeout=PERIOD)
        if len(requests) > MAX_REQUEST_PER_MINIUTE:
            return HttpResponse("请求过于频繁，请稍后重试")
