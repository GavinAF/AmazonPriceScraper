from django.http import HttpResponse

def index(request):
    output = "Amazon Price Scraper"
    return HttpResponse(output)