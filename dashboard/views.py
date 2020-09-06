from django.shortcuts import render


# Create your views here.
def test_view(request):
    return render(request, template_name='dboards/test_temp.html')


def test_maps(request):
    return render(request, template_name='dboards/ui-maps.html')


def test_index(request):
    return render(request, template_name='dboards/test_index.html')


def test_notifications(request):
    return render(request, template_name='dboards/test_notifications.html')