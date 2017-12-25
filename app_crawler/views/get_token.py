from app_crawler.storage.huadao import token
from django.http import JsonResponse
from crawler.settings import logger

# getToken
def getHDToken(request)->JsonResponse:
    t = token.tokenUpdate()
    res = t.main()
    logger.info("execute getHDToken")
    return JsonResponse(res)