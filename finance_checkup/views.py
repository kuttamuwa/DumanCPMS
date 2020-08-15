from django.shortcuts import render

# Create your views here.
from rest_framework import authentication, permissions
from rest_framework.views import APIView

"""
Uyarılar
Çek endeksi verisi istenmeyen aralıkta ise uyarı verilir
Arkası yazılı çekler varsa uyarı verilir
Kredi limiti daralanlar-kapatılanlar uyarı
Findeks Kredi notu
Karekodlu Çek Skoruna paralel uyarı verilir
NOTIFICATION’LAR SADECE NOTIFICATION DEĞİL; TEPKİ DE VEREBİLECEĞİ BUTONA BASABİLECEĞİ BİR ŞEY OLMASI GEREK.
Mesaj ve mail altyapıları yapılacak.

Entegrasyon
KKB entegrasyon altyapısına paralel Findeks menüden müşteri bilgisi girilir, sistemden gelen pdf raporundan 
ilgili veriler buraya yazılır 
Yazılan veri tarih damgası ile arşivde saklanır 
Bu ekranda da son 5 rapor verisi altlata gösterilir

"""


# some pages
def finance_checkup_page(request):
    return render(request, 'finance_checkup/main_page.html')


def api_guide(request):
    return render(request, 'finance_checkup/api_guide.html')


class RiskReportSummary(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    """
        Ticari Limit Risk Özet Bilgileri
        Kurum Bazında Detaylı Limit / Risk Bilgileri
        Kaç Banka ile Çalışıldığı
        Son Kredi Kullanım Tarihi
        En Güncel Limit Tahsis Tarihi
        Leasing Canlı Krediler
        Faktoring Canlı Krediler
        Takibe Alınmış Banka Kredileri
        Takibe Alınmış Leasing Kredileri
        Takibe Alınmış Faktoring Kredileri
    """

    def get(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        return True


class CheckReportSummary(APIView):
    """
    Karekodlu Çek Skoru
    Çek Endeksi
    Türkiye ortalamasına göre durumu
    Zamanında ödenen çeklerin toplam adet ve tutarları (1,3,6 ve 12 aylık dağılımı)
    Gecikmeli ödenen çeklerin toplam adet ve tutarları (1,3,6 ve 12 aylık dağılımı)
    Karşılıksız çeklerin toplam adet ve tutarları (1,3,6 ve 12 aylık dağılımı)
    Açık çek bilgileri
    İleri vadeli çek bilgileri
    Çek hesabı olan bankalar
    Arkası yazılı çekler

    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return True

    def post(self, request, format=None):
        return True


class GuaranteeLetterStateSummary(APIView):
    """
    Muhatap
    Lehtar
    Vade bilgisi
    Vade tarihi
    Düzenlenme tarihi
    Mektubun orijinal tutarı
    Mektup bakiyesi
    Banka adı
    Şube adı
    Sorgu tarihi

    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return True


class FindeksRiskReport(APIView):
    """
    •    Findeks Kredi Notu (Notlu Risk Raporu aldığınızda, kredi notunuz da raporda yer alır.)
    •    Kredi notunun değişimi
    •    Kredi notunun Türkiye ortalamasıyla karşılaştırması
    •    Kaç adet kredili ürüne sahip olunduğu ve ürün çeşitleri (kredi, kredi kartı ve kredili mevduat hesabı)
    •    Tüm bankalardaki kredili ürünlerinizin toplam limit ve borç bilgileri 
    •    Kredili ürünlerinizin açık/kapalı olduğu bilgisi
    •    Kredili ürünlerinizdeki geçmiş ödeme performansı

    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return True
