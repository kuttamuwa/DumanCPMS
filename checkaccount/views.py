from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from rest_framework import status
from rest_framework.views import APIView

from checkaccount.forms import CheckAccountCreateForm
from checkaccount.models import CheckAccount
from checkaccount.serializers import CheckAccountSerializer
from .filters import CheckAccountFilter


def main_page(request):
    return render(request, 'base.html')


checkaccount_shown_fields = [i.name for i in CheckAccount._meta.get_fields() if i not in CheckAccount.get_auto_fields()]


# Site views
def checkaccount_mainpage(request):
    return render(request, 'checkaccount/checkaccount_main.html')


def checkaccount_loginpage(request):
    if request.method == 'GET':
        # context = {'form': }
        return render(request, 'checkaccount/registration/login.html')

    elif request.method == 'POST':
        usr = request


@login_required(login_url='/checkaccount/loginapp')
def check_account_search(request):
    checkaccount = CheckAccount.objects.all()
    print(f"check account : {checkaccount}")

    account_filter = CheckAccountFilter(request.GET)

    context = {'checkaccount': checkaccount,
               'account_filter': account_filter,
               }

    return render(request, context=context, template_name='checkaccount/account_with_filter.html')


# API VIEW
class CheckAccountAPI(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'templates/abc.html'

    def get(self, request, format=None):
        snippets = CheckAccount.objects.all()
        serializer = CheckAccountSerializer(snippets, many=True)
        return JsonResponse(dict(serializer.data[0]), status=201)

    def post(self, request, format=None):
        serializer = CheckAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAccountFormView(View):
    form_class = CheckAccountCreateForm
    initial = {'key': 'value'}
    template_name = 'checkaccount/checkaccount_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


class CheckAccountFormCreateView(CreateView):  # , LoginRequiredMixin):
    template_name = 'checkaccount/checkaccount_form.html'
    # form_class = CheckAccountForm
    # success_url = 'checkaccount/succeeded_form.html'
    model = CheckAccount

    fields = '__all__'

    def form_valid(self, form):
        print("form took")
        return super().form_valid(form)


class CheckAccountFormDeleteView(DeleteView):
    model = CheckAccount
    # fields = checkaccount_shown_fields


class CheckAccountFormUpdateView(UpdateView):
    # model = CheckAccountCreateForm
    fields = checkaccount_shown_fields


class CheckAccountSearchView(ListView):
    model = CheckAccount
    template_name = 'checkaccount/searchresults.html'


def NotImplementedPage(request):
    return render(request, 'checkaccount/not_implemented_yet.html')
