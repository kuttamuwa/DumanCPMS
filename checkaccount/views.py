from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from rest_framework import status
from rest_framework.views import APIView

# from checkaccount.forms import CheckAccountForm
# from checkaccount.forms import CheckAccountForm
from checkaccount.models import CheckAccount
from checkaccount.serializers import CheckAccountSerializer


def main_page(request):
    return render(request, 'base.html')


checkaccount_shown_fields = [i.name for i in CheckAccount._meta.get_fields() if i not in CheckAccount.get_auto_fields()]


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


class CheckAccountFormView(FormView):
    template_name = 'checkaccount/checkaccount_form.html'
    # form_class = CheckAccountForm
    model = CheckAccount
    fields = ('firm_type',
              'firm_full_name',)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


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
    # model = CheckAccountForm
    fields = checkaccount_shown_fields
