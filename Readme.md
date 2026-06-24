# 🕊️ Riemann Analizi

Doğanın pürüzsüz ve sürekli akışını, sakin matematiksel adımlarla ayrık parçalara bölerek inceleyen minimalist bir kalkülüs laboratuvarı. Bu proje; Sol Riemann, Sağ Riemann, Orta Nokta ve Yamuk Yöntemi gibi entegrasyon yaklaşımlarını gözü yormayan soft pastel tonlarla görselleştirir ve asimptotik hata analizlerini sunar.

---

## ✨ Özellikler

* **Yumuşak ve Dingin Arayüz:** Gözü yoran yanar döner efektlerden ve keskin hatlardan uzak, mat fildişi ve soft vizon tonlarında minimalist tasarım.
* **Dinamik Matematik Motoru:** Hazır monoton/konveks/konkav fonksiyon şablonlarının yanı sıra, kendi matematiksel fonksiyonlarınızı yazabileceğiniz esnek altyapı.
* **Geometrik Görselleştirme:** Seçilen fonksiyonun alt bölme sayılarına ($n$) göre alan yaklaşımlarını canlı ve soft grafiklerle çizim imkanı.
* **Asimptotik Hata Analizi:** Bölme sayısı sonsuza ($n \to \infty$) doğru yaklaşırken hata paylarının sıfır doğrusuna nasıl asimptotik olarak yakınsadığını gösteren logaritmik simülasyon grafiği.

---

## 🛠️ Kurulum ve Yerel Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak isterseniz aşağıdaki adımları takip edebilirsiniz:

1.  **Depoyu bilgisayarınıza indirin:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/riemann-analizi.git](https://github.com/KULLANICI_ADINIZ/riemann-analizi.git)
    cd riemann-analizi
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı başlatın:**
    ```bash
    streamlit run app.py
    ```

---

## 📦 Bağımlılıklar (Requirements)

Projenin pürüzsüz çalışabilmesi için `requirements.txt` dosyasında yer alan temel kütüphaneler:
* `streamlit`
* `numpy`
* `matplotlib`
* `scipy`
* `pandas`

---

## 🧠 Perde Arkası

Bilgisayarlar doğadaki sürekli (continuous) eğrileri ancak sonsuz küçük ayrık (discrete) parçalara bölerek taklit edebilir. Bölme sayısı ($n$) arttıkça, Riemann Toplamı asimptotik olarak analitik integral alanına evrilir:

$$\lim_{n \to \infty} \sum_{i=1}^{n} f(x_i) \Delta x = \int_{a}^{b} f(x) dx$$S