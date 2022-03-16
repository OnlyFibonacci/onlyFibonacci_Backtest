from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta

client = Client(None, None)


def verileriGetir(sembol, periyot, baslangic, bitis):
    mumlar = client.get_historical_klines(sembol, periyot, baslangic, bitis)
    return mumlar


def csvOlustur(sembol, mumlar):
    csvDosya = open(sembol + "1_DAY.csv", 'w', newline='')
    yazici = csv.writer(csvDosya, delimiter=',')
    for mumVerileri in mumlar:
        yazici.writerow(mumVerileri)
    csvDosya.close()


def veriCekmeVeCsvOlusturma():
    semboller = ["XRPUSDT", "ATOMUSDT", "COMPUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT"]
    for coin in semboller:
        csvOlustur(coin, verileriGetir(coin, Client.KLINE_INTERVAL_1DAY, "6 March 2018", "5 March 2022"))
        print(coin, " Verileri Getirildi.")


def zamanHesapla(timestamp):
    return dt.fromtimestamp(timestamp / 1000)


def alSAT():
    cuzdan = 100
    alimSayisi = 0
    satimSayisi = 0
    toplamCoin = 0
    komisyonOrani = 75 / 10000
    verilenKomisyon = 0
    okunacakCsv = 'BTCUSDT.csv'
    basliklar = ['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbav', 'tbqav',
                 'ignore']
    df = pd.read_csv(okunacakCsv, names=basliklar)
    open = df['open']
    close = df['close']
    high = df['high']
    low = df['low']

    acilisZamani = df['open_time']
    sma50 = ta.ma("sma", close, length=50)
    sma200 = ta.ma("sma", close, length=200)

    print("#### BAŞLIYORUZZZZZ ONLY FIBONACCI'yi takip ediniz #############")
    for i in range(len(close)):
        if pd.isna(sma50[i]) is False:

            # if close[i-1] < sma50[i-1] and close[i] > sma50[i]: # yukarı kesişim fonksiyonu
            if sma50[i - 1] < sma200[i - 1] and sma50[i] > sma200[i]:  # yukarı kesişim fonksiyonu
                print(zamanHesapla(acilisZamani[i + 1]), " tarihinde ", cuzdan / close[i], " adet BTC alındı")
                print("#################")
                alimSayisi += 1
                toplamCoin = cuzdan / close[i]
                verilenKomisyon += komisyonOrani * cuzdan
            if sma50[i - 1] > sma200[i - 1] and sma50[i] < sma200[i] and alimSayisi > 0:  # aşağı kesişim fonksiyonu
                print(zamanHesapla(acilisZamani[i + 1]), " tarihinde ", toplamCoin, " adet BTC satıldı")
                satimSayisi += 1
                fiyat = close[i] * toplamCoin
                cuzdan = fiyat
                toplamCoin = 0
                verilenKomisyon += komisyonOrani * fiyat
                print(f"Bu iki işlem sonucundaki cüzdan ederi : {cuzdan}")
                print("#################")

    print(f"Toplam Yapılan İşlem : {alimSayisi + satimSayisi}")
    print(f"Toplam Verilen Komisyon : {verilenKomisyon}")
    print(f"Total Cüzdan : {cuzdan}")


alSAT()