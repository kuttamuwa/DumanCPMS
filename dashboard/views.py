# from django.http import JsonResponse
# from django.shortcuts import render
#
# from checkaccount.models import CheckAccount
# from dashboard.models import Order
# from django.core import serializers
#
# from risk_analysis.models import DataSetModel
#
#
# def dashboard_with_pivot(request):
#     return render(request, 'dboards/dashboard_with_pivot.html', {})
#
#
# def pivot_data(request):
#     dataset = Order.objects.all()
#     data = serializers.serialize('json', dataset)
#     return JsonResponse(data, safe=False)
#
#
# # Create your views here.
# def test_view(request):
#     return render(request, template_name='dboards/test_temp.html')
#
#
# def test_maps(request):
#     return render(request, template_name='dboards/ui-maps.html')
#
#
# def test_index(request):
#     return render(request, template_name='dboards/test_index.html')
#
#
# def test_notifications(request):
#     return render(request, template_name='dboards/test_notifications.html')
#
#
# def find_exceeds_limit(request):
#     pass
#
#
# def find_exceeds_maturity(request):
#     pass
#
#
# def find_worst_performance(request):
#     """
#     Alacak devir hızı (en kotu performans)
#     """
#     pass
#
#
# def warn_check_index_data(request):
#     """
#     Çek endeksi verisi istenmeyen aralıkta ise uyarı verilir
#     """
#     pass
#
#
# def find_behind_written_checks(request):
#     """
#     Arkası yazılı çekler varsa uyarı verilir
#     """
#     pass
#
#
# def warn_credit_limit_narrowing(request):
#     """
#     Kredi limiti daralanlar-kapatılanlar uyarı
#     """
#     pass
#
#
# def warn_tax_debt(request):
#     """
#     Vergi borcu Uyarılar
#     """
#     pass
#
#
# def warn_sgk_debts(request):
#     """
#     SGK Borcu Uyarılar
#     """
#     pass
#
#
# def warn_black_list_sector(request, sector_name):
#     """
#     Sektör Kara Liste
#     """
#     pass
#
#
# def findeks_credit_note(request):
#     """
#     Findeks Kredi notu
#     """
#     pass
#
#
# def warn_qr_check_score(request):
#     """
#     Karekodlu Çek Skoruna paralel uyarı verilir
#     """
#     pass
#
#
# def get_newest_check_accounts(request, count=5):
#     """
#     Yeni eklenen müşteriler
#     """
#     accounts = CheckAccount.objects.all()[:count]
#     print(accounts)
#     data_set = DataSetModel.objects.all().filter(customer_id__in=(i.related_customer for i in accounts))
#
#     data = {'customer_names': (i.firm_full_name for i in accounts),
#             'limit': (i.limit for i in data_set),
#             'warrant_state': (i.warrant_state for i in data_set),
#             'birthplace': (i.city for i in accounts)}
#
#     context = {'data': data}
#
#     # (Müşteri Adı, Limit, Teminat Durumu, İl)
#     return render(request, 'dboards/checkaccounts/get_latest_accounts.html', context=context)
