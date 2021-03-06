
"""

Burası resimden ndvı analizi



"""
#https://cihanbosnali.com/posts/opencv_goruntu_isleme_3.html
#https://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/using-tools-in-python.htm burayı da kullan
#güzel indirme linki https://tpm-ds.eo.esa.int/smcat/RapidEyeSentinel/3/W054/S25/0/
import rasterio
import numpy as np
#dosya adını giriyoruz
dosya=("20160928_020256_SSC1d3_0013_L3A_pansharp")
konum=("pansharpened")
Dosya_adi=("skysattif/"+konum+"/"+dosya+".tif")
# rasterio ile açıp renk spektrumlarına ayırıyoruz
with rasterio.open(Dosya_adi) as src:
    band_red = src.read(2)

with rasterio.open(Dosya_adi) as src:
    band_nir = src.read(4)
    

# Klasik NDVI denklemi ile hesaplama
np.seterr(divide='ignore', invalid='ignore')

# Calculate NDVI. This is the equation at the top of this guide expressed in code
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
#su için yapıyorum bu analizi
##
###
ndvi=(band_red.astype(float) - band_nir.astype(float)) / (band_red + band_nir)
###
###
np.nanmin(ndvi), np.nanmax(ndvi)
    


kwargs = src.meta
kwargs.update(
    dtype=rasterio.float32,
    count = 1)

# Raster oluşturuyoruz

ras_open='skysattif/donusumler/'+'karartma '+dosya+'.tif'
with rasterio.open(ras_open, 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))

# görüntümüze bakalım renklerine ayrılmış bir görüntümüz var
# çizim yapacağız bunun için gerekli kütüphaneler ekleniyor

import matplotlib.pyplot as plt
import matplotlib.colors as colors

# NDVI bilindiği üzere 1 ve -1 arasındaki değerlerde sınıflandırılır.
# Biz de bu değerleri renklerle göstermek istiyoruz.
# Bunun için alınan sayısal değerleri farklı renk spektrumlarına atayarak elimizde NDVI için renklendirilmiş bir görüntümüz olacaktır
# 
# Bir orta nokta belirledik ve bu sola ve sağa olacak şekilde renklendiriyoru renk spekturumunu da aşağıda paylaşacağım

class RenkNormalizasyonu(colors.Normalize):
   
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):

        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

min=np.nanmin(ndvi)
max=np.nanmax(ndvi)
mid=0.1

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

cmap = plt.cm.RdYlGn 

cax = ax.imshow(ndvi, cmap=cmap, clim=(min, max), norm=RenkNormalizasyonu(midpoint=mid,vmin=min, vmax=max))

ax.axis('off')
ax.set_title('NDVI görüntüsü', fontsize=18, fontweight='bold')

cbar = fig.colorbar(cax, orientation='horizontal', shrink=0.65)
fig_kaydet="skysattif/donusumler/"+"figure  "+dosya+".png"
fig.savefig(fig_kaydet, dpi=200, bbox_inches='tight', pad_inches=0.7)

plt.show()




fig2 = plt.figure(figsize=(10,10))
ax = fig2.add_subplot(111)

plt.title("NDVI Histogram", fontsize=18, fontweight='bold')
plt.xlabel("NDVI values", fontsize=14)
plt.ylabel("# pixels", fontsize=14)


x = ndvi[~np.isnan(ndvi)]
numBins = 20
ax.hist(x,numBins,color='black',alpha=1)
dosya=("20170724_184829_ssc2d1_0004_L3A_pansharp")
histog_kaydet="skysattif/donusumler/"+"histogram    "+dosya+".png"
fig2.savefig(histog_kaydet, dpi=200, bbox_inches='tight', pad_inches=0.7)

plt.show()


"""
from scipy.stats import skew
print (skew(x))
np.mean(x)
"""


"""

2. part burada

burada görüntü işleme ile ne durumda olduğunu bulacağız

"""
import cv2
#burası 1 kere yapılması gerekiyor
resim = cv2.imread(histog_kaydet,111)
cv2.imwrite("skysattif/donusumler//goruntu_isleme/resim_yenimis.jpg",resim)

resim_yeni="skysattif/donusumler//goruntu_isleme/resim_yenimis.jpg"
import cv2
import numpy as np

resim = cv2.imread(resim_yeni)


#bölge seçmeyi yapıyorum

#burası 1.seviye kurak alan oluyor
kesilmis_karek1= resim[0:157,0:161]
# burası 2. seviye kurak alan
kesilmis_karek2= resim[0:238,0:161]
# burası 3. seviye kurak alan
kesilmis_karek3= resim[0:422,0:161]

#burası 1.seviye az yeşil alan oluyor
kesilmis_kareaz1= resim[0:157,162:277]
# burası 2. seviye az yeşil alan
kesilmis_kareaz2= resim[0:238,162:277]
# burası 3. seviye az yeşil alan
kesilmis_kareaz3= resim[0:422,162:277]

#burası 1.seviye çok yeşil alan oluyor
kesilmis_karey1= resim[0:157,278:462]
# burası 2. seviye az yeşil alan
kesilmis_karey2= resim[0:238,278:462]
# burası 3. seviye az yeşil alan
kesilmis_karey3= resim[0:422,278:462]

#listemelemek için

listem_ort=[]

kesilmis_karek1_ort=np.mean(kesilmis_karek1)
listem_ort.append(kesilmis_karek1_ort)

kesilmis_karek2_ort=np.mean(kesilmis_karek2)
listem_ort.append(kesilmis_karek2_ort)

kesilmis_karek3_ort=np.mean(kesilmis_karek3)
listem_ort.append(kesilmis_karek3_ort)

kesilmis_kareaz1_ort=np.mean(kesilmis_kareaz1)
listem_ort.append(kesilmis_kareaz1_ort)

kesilmis_kareaz2_ort=np.mean(kesilmis_kareaz2) 
listem_ort.append(kesilmis_kareaz2_ort)

kesilmis_kareaz3_ort=np.mean(kesilmis_kareaz3) 
listem_ort.append(kesilmis_kareaz3_ort)

kesilmis_karey1_ort=np.mean(kesilmis_karey1)
listem_ort.append(kesilmis_karey1_ort)

kesilmis_karey2_ort=np.mean(kesilmis_karey2)
listem_ort.append(kesilmis_karey2_ort)

kesilmis_karey3_ort=np.mean(kesilmis_karey3)
listem_ort.append(kesilmis_karey3_ort)




# yoğunluk hesaplandı
listem_ort.sort()
en_kucuk=listem_ort[0]
if en_kucuk==kesilmis_karek1_ort:
    toprak_turu="kuraklık seviyesi 1"
elif en_kucuk==kesilmis_karek2_ort:
   toprak_turu="kuraklık seviyesi 2"
elif en_kucuk==kesilmis_karek3_ort:
    toprak_turu="kuraklık seviyesi 3"
elif en_kucuk==kesilmis_kareaz1_ort:
    toprak_turu="Az yeşil 1"
elif en_kucuk==kesilmis_kareaz2_ort:
    toprak_turu="Az yeşil 2"
elif en_kucuk==kesilmis_kareaz3_ort:
    toprak_turu="Az yeşil 3"
elif en_kucuk==kesilmis_karey1_ort:
    toprak_turu="Yeşil 1"
elif en_kucuk==kesilmis_karey2_ort:
    toprak_turu="Yeşil 2"
elif en_kucuk==kesilmis_karey3_ort:
    toprak_turu="Yeşil 3"
print("1 en yüksek değeri ifade eder yeşil 1 en fazla yeşillik, kuraklık 1 en kurak alan anlamına gelir")
print("yoğunluk olarak: %s"%toprak_turu)
    

#ortalama hesaplanıyor
#burda en yakın komşuyu buluyoruz
from heapq import nsmallest
ortalama_yogunluk=nsmallest(1, listem_ort, key=lambda x: abs(x-(np.sum(listem_ort)/9)))

if ortalama_yogunluk==kesilmis_karek1_ort:
    yogunluk_tipi="kuraklık seviyesi 1"
elif ortalama_yogunluk==kesilmis_karek2_ort:
   yogunluk_tipi="kuraklık seviyesi 2"
elif ortalama_yogunluk==kesilmis_karek3_ort:
    yogunluk_tipi="kuraklık seviyesi 3"
elif ortalama_yogunluk==kesilmis_kareaz1_ort:
    yogunluk_tipi="Az yeşil 1"
elif ortalama_yogunluk==kesilmis_kareaz2_ort:
    yogunluk_tipi="Az yeşil 2"
elif ortalama_yogunluk==kesilmis_kareaz3_ort:
    yogunluk_tipi="Az yeşil 3"
elif ortalama_yogunluk==kesilmis_karey1_ort:
    yogunluk_tipi="Yeşil 1"
elif ortalama_yogunluk==kesilmis_karey2_ort:
    yogunluk_tipi="Yeşil 2"
elif ortalama_yogunluk==kesilmis_karey3_ort:
    yogunluk_tipi="Yeşil 3"
print("1 en yüksek değeri ifade eder yeşil 1 en fazla yeşillik, kuraklık 1 en kurak alan anlamına gelir")
print("ortalama olarak: %s"%yogunluk_tipi)
print("yoğunluk olarak: %s"%toprak_turu)




"""
Burası bölünen alanları görmek için var yok sayılabilir

"""


"""
#gösterme kesilmiş kare kurak alan 
cv2.imshow("kesilmis_karek1",kesilmis_karek1)
cv2.imshow("kesilmis_karek2",kesilmis_karek2)
cv2.imshow("kesilmis_karek3",kesilmis_karek3)

#gösterme kesilmiş az yeşil alan 
cv2.imshow("kesilmis_kareaz1",kesilmis_kareaz1)
cv2.imshow("kesilmis_kareaz2",kesilmis_kareaz2)
cv2.imshow("kesilmis_kareaz3",kesilmis_kareaz3)

#gösterme kesilmiş çok yeşil alan
cv2.imshow("kesilmis_karey1",kesilmis_karey1)
cv2.imshow("kesilmis_karey2",kesilmis_karey2)
cv2.imshow("kesilmis_karey3",kesilmis_karey3)

cv2.waitKey(0)
cv2. destroyAllWindows()
type(resim)
"""


# pasta grafiğine dönüştürüyoruz 

import matplotlib.pyplot as plt

%matplotlib inline


labels="kuraklık seviyesi 1","kuraklık seviyesi 2","kuraklık seviyesi 3","Az yeşil 1","Az yeşil 2","Az yeşil 3","Yeşil 1","Yeşil 2","Yeşil 3"
sizes=[kesilmis_karek1_ort,kesilmis_karek2_ort,kesilmis_karek3_ort,kesilmis_kareaz1_ort,kesilmis_kareaz2_ort,kesilmis_kareaz3_ort,kesilmis_karey1_ort,kesilmis_karey2_ort,kesilmis_karey3_ort]
explode = (0,0,0,0.2,0.2,0.2,0,0.1,0)

figl, axl = plt.subplots()

axl.pie(sizes,explode=explode,labels=labels,autopct="%1.1f%%", shadow=True, startangle=90)
axl.axis("equal")
figl.savefig("pasta_grafik.png")
plt.show()




"""

Bu kısımda ise isimlendirme yapacağız

ara verdim yarın bakarım

"""

import numpy as np
import cv2
import pandas as pd
resim_yeni="skysattif/donusumler/goruntu_isleme/denemeresmim.png"
#burası 1 kere yapılması gerekiyor
resim = cv2.imread(resim_yeni)


a=cv2.cvtColor(resim,cv2.COLOR_RGB2BGR) #MAVİ
b=a+resim

lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])

mask = cv2.inRange(a, lower_red, upper_red)
res = cv2.bitwise_and(a,a, mask= mask)

res


np.mean(kesilmis_kareaz2)


bas=(0,0)
bit=(92,180)
deneme_kare=cv2.rectangle(kesilmis_kareaz2,bas,bit,(0, 255, 0),20)

font = cv2.FONT_HERSHEY_SIMPLEX 
yazi=cv2.putText(deneme_kare,"deneme",(0,50),font,1,(0,0,0),2,)
cv2.imwrite("deneme3.png",deneme_kare)
cv2.imwrite("yazili.png",yazi)

histog_kaydet="skysattif/donusumler/figure20160928_020256_SSC1d3_0013_L3A_pansharp.png"
resim = cv2.imread(histog_kaydet)
hsv = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)
lower = np.array([50,40,35])
upper = np.array([85,255,255])
mask = cv2.inRange(hsv, lower, upper)
cv2.imwrite("masklandı.png",mask)

#bölge seçmeyi yapıyorum"""
#burası 1.seviye kurak alan oluyor
kesilmis_karek1= resim[0:104,0:94]
# burası 2. seviye kurak alan
kesilmis_karek2= resim[104:208,0:94]
# burası 3. seviye kurak alan
kesilmis_karek3= resim[209:312,0:94]

#burası 1.seviye az yeşil alan oluyor
kesilmis_kareaz1= resim[0:104,94:188]
# burası 2. seviye az yeşil alan
kesilmis_kareaz2= resim[104:208,94:188]
# burası 3. seviye az yeşil alan
kesilmis_kareaz3= resim[209:312,94:188]

#burası 1.seviye çok yeşil alan oluyor
kesilmis_karey1= resim[0:104,188:288]
# burası 2. seviye az yeşil alan
kesilmis_karey2= resim[104:208,188:288]
# burası 3. seviye az yeşil alan
kesilmis_karey3= resim[209:312,188:288]


#gösterme kesilmiş kare kurak alan 
cv2.imshow("kesilmis_karek1",kesilmis_karek1)
cv2.imshow("kesilmis_karek2",kesilmis_karek2)
cv2.imshow("kesilmis_karek3",kesilmis_karek3)

#gösterme kesilmiş az yeşil alan 
cv2.imshow("kesilmis_kareaz1",kesilmis_kareaz1)
cv2.imshow("kesilmis_kareaz2",kesilmis_kareaz2)
cv2.imshow("kesilmis_kareaz3",kesilmis_kareaz3)

#gösterme kesilmiş çok yeşil alan
cv2.imshow("kesilmis_karey1",kesilmis_karey1)
cv2.imshow("kesilmis_karey2",kesilmis_karey2)
cv2.imshow("kesilmis_karey3",kesilmis_karey3)



cv2.waitKey(0)
cv2. destroyAllWindows()
type(resim)


import numpy as np
import argparse
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["resim"])

#kulllan burayı
"""
https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
"""

cv2.waitKey(0)
cv2. destroyAllWindows()
type(resim)


