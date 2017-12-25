from app_crawler.case_test.infos_emd008 import infos_emd008_test
from django.http import HttpResponse

def emd008_test(request):
    infos_emd008_test()
    return HttpResponse("ok,run over")