from django.http import HttpResponse

def send_status(status):
    return HttpResponse(status=status)
