from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(request, 'home/main_page.html')


def contact_page(request):
    return render(request, 'home/contact_page.html')
