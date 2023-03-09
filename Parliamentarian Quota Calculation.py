# Sığmayan yorum satırları yorum gerekn kısımların üstlerine yazılmıştır.
# Main fonksiyonu bütün fonksiyonların sıralı çalışmasını sağlarken hata kontrolü ve liste başlatmalarını da yapar.
def main():
    try:
        file = open("secim.txt", "r")
        parti_sayisi = int(file.readline())
        il_sayisi = len(file.readlines()) // (parti_sayisi + 2)
    except IOError:
        print("Dosya açılamadı")
    except ValueError:
        print("Parti sayısı sayısal olarak girilmedi.")
    else:
        file.seek(0)  # okumayı başa sarar
        file.readline()  # Okurken ilk satırın atlanmasını sağlar.
        top_oy_say = [0] * parti_sayisi  # Partilerin ülke geneli toplam oy sayıları için liste başlatır.
        mv_top = [0] * parti_sayisi  # Partilerin ülke geneli toplam  milletvekili sayıları için liste başlatır.
        # Partilerin ülke geneli toplam hiç aday çıkaramadıkları il sayısı için liste başlatır.
        mv_sifir = [0] * parti_sayisi
        genel_top_oy = 0  # Türkiye geneli toplam geçerli oy sayısı için sayacı başlatır
        top_kontenjan = 0  # Türkiye geneli toplam millet vekili kontenjanı için sayacı başlatır
        for il in range(il_sayisi):  # Her bir il için yapılacak işlemleri döndürür.
            mv_il = [0] * parti_sayisi  # Partilerin il başına toplam oy sayıları için liste başlatır.
            # Fonksiyonlar çağırılır.
            plaka = plaka_al(file)
            kontenjan = kontenjan_al(file)
            liste = listele(parti_sayisi, file)
            mv_il = il_mv_sayisi_bul(kontenjan, liste, mv_il)
            genel_top_oy, top_kontenjan = \
                il_tablo(plaka, kontenjan, liste, mv_il, parti_sayisi, genel_top_oy, top_kontenjan)
            # Eleman sayısı kadar döndürülerek gerekli listelere gerekli değerler verilir.
            for say in range(len(liste)):
                top_oy_say[say] += liste[say]
            for say in range(len(mv_il)):
                mv_top[say] += mv_il[say]
                if mv_il[say] == 0:
                    mv_sifir[say] += 1
        genel_tablo(genel_top_oy, parti_sayisi, mv_top, top_oy_say, mv_sifir, top_kontenjan)
        file.close()


def plaka_al(file):  # İl plaka numarasını alır.
    plaka = (file.readline())
    return plaka


def kontenjan_al(file):  # İl başına milliet vekili kontenjanı alır
    kontenjan = int(file.readline())
    return kontenjan


def parti_oy_sayisi_al(file):  # İl başına partilere verilen oyları alır
    parti_oy_sayisi = int(file.readline())
    return parti_oy_sayisi


def listele(parti_sayisi, file):  # İl başına tüm değerleri partilere bölerek listeler
    liste = []
    for b in range(parti_sayisi):
        liste.append(parti_oy_sayisi_al(file))
    return liste


# İlde parti başına millet vekili sayısını verilen hesaplamayı kullanarak bulur.
def il_mv_sayisi_bul(kontenjan, liste, mv_il):
    olu_liste = list(liste)
    for milletvekili in range(int(kontenjan)):
        yuksek_oylu = max(olu_liste)
        index = olu_liste.index(yuksek_oylu)
        olu_liste[index] = yuksek_oylu // 2
        mv_il[index] += 1

    return mv_il


# İl başına tabloyu hesaplayarak yazdırırken Tükiye Geneli tablo için gerekli olan sayaçlara eklemeler yapar.
def il_tablo(plaka, kontenjan, liste, mv_il, parti_sayisi, top_kontenjan, genel_top_oy):
    top_oy = 0

    print("İl plaka kodu: " + str(plaka), end="")
    print("Milletvekili Kontenjani: " + str(kontenjan))
    for parti in range(parti_sayisi):
        top_oy += liste[parti]
    print("Gecerli Oy Sayisi: " + str(top_oy))
    print("Pusula Sira Oy Say Oy Yuzde MV Say")
    print("----------- ------ -------- ------")
    for say in range(parti_sayisi):
        print(format(say + 1, "11d"), end=" ")
        print(format(liste[say], "6d"), end=" ")
        print(format(liste[say] / top_oy * 100, "8.2f"), end=" ")
        print(format(mv_il[say], "6d"))
    print()
    genel_top_oy += top_oy
    top_kontenjan += kontenjan
    return genel_top_oy, top_kontenjan


# Türkiye geneli tabloyu hesaplar ve yazdırır
def genel_tablo(genel_top_oy, parti_sayisi, mv_top, top_oy_say, mv_sifir, top_kontenjan):
    toplam_mv = sum(mv_top)
    print("Türkiye Geneli")
    print("Milletvekili Kontenjani: ", top_kontenjan)

    print("Gecerli Oy Sayisi: " + str(genel_top_oy))
    print("Pusula Sira Oy Say Oy Yuzde MV Say MV Yuzde 0 MV Il Say")
    print("----------- ------ -------- ------ -------- -----------")
    for sayi in range(parti_sayisi):
        print(format(sayi + 1, "11d"), end=" ")
        print(format(top_oy_say[sayi], "6d"), end=" ")
        print(format(top_oy_say[sayi] / genel_top_oy * 100, "8.2f"), end=" ")
        print(format(mv_top[sayi], "6d"), end=" ")
        print(format(mv_top[sayi] / toplam_mv * 100, "8.2f"), end=" ")
        print(format(mv_sifir[sayi], "11d"))


main()
