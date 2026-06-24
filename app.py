import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import pandas as pd
import re

# ==========================================================
# 🎨 1. MAT PASTEL VE DİNGİN SOFT CSS ENJEKSİYONU
# ==========================================================
st.set_page_config(page_title="Riemann Analizi", layout="wide")

st.markdown("""
<style>
    /* Ana arka plan: Dingin, yumuşak mat fildişi / süt beyazı */
    .stApp {
        background-color: #f7f6f2;
        color: #2c3e50; /* Yumuşak antrasit okuma rengi */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sol Panel (Sidebar): Soft mat vizon / gri bej */
    section[data-testid="stSidebar"] {
        background-color: #eae7df !important;
        border-right: 1px solid #d3cfc4;
    }
    
    /* Sol paneldeki yazılar */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label {
        color: #4a5568 !important;
    }
    
    /* 🕊️ SOFT VE SABİT LOGO TASARIMI */
    .badge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
    .badge-arma {
        border: 1px solid #c8c3b4;
        padding: 14px 45px;
        border-radius: 40px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        display: inline-block;
    }

    .project-logo {
        font-size: 2.2em;
        font-weight: 600;
        letter-spacing: -0.5px;
        text-align: center;
        color: #2c3e50;
    }
    
    /* Başlıklar */
    h2, h3 {
        color: #2c3e50 !important;
        font-weight: 500;
        letter-spacing: -0.5px;
    }
    
    /* Sekme (Tab) Tasarımları: Yumuşatılmış Köşeler */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #eae7df;
        border: 1px solid #d3cfc4;
        border-radius: 20px 20px 0px 0px;
        color: #626d71;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border-bottom: 2px solid #ffffff !important;
    }
    
    /* Yumuşak Pastel Kartlar */
    .ai-card {
        background: #ffffff;
        border: 1px solid #e3dec9;
        border-left: 4px solid #a3b899; /* Soft Adaçayı Yeşili */
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .trivia-card {
        background: #ffffff;
        border: 1px solid #e3dec9;
        border-left: 4px solid #b2c4db; /* Soft Puslu Mavi */
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .ouverture-card {
        background: #faf8f5;
        border: 1px solid #e6dfd3;
        border-left: 4px solid #cca4a4; /* Soft Gül Kurusu */
        padding: 24px;
        border-radius: 8px;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 🧠 2. ARKA PLAN MANTIĞI VE MATEMATİK MOTORU
# ==========================================================

st.markdown("""
<div class='badge-container'>
    <div class='badge-arma'>
        <div class='project-logo'>
            RİEMANN ANALİZİ
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #7f8c8d; font-style: italic; margin-top: -15px;'>Doğanın pürüzsüz akışını, sakin matematiksel adımlarla parçalama alanı.</p>", unsafe_allow_html=True)
st.write("---")

# Yan Menü Tasarımı
st.sidebar.markdown("## 🛠️ Üs Ayarları")

hazir_fonksiyonlar = {
    "Kendi Fonksiyonumu Yazacağım ✍️": None,
    "Monoton Artan: x^2": "x**2",
    "Monoton Azalan: e^(-x)": "np.exp(-x)",
    "Konveks: e^x": "np.exp(x)",
    "Konkav: sqrt(x)": "np.sqrt(x)",
    "Yüksek Salınımlı: |sin(5x)|": "np.abs(np.sin(5*x))"
}

secilen_hazir = st.sidebar.selectbox("Hazır Şablonlar:", list(hazir_fonksiyonlar.keys()))

if secilen_hazir == "Kendi Fonksiyonumu Yazacağım ✍️":
    kullanici_girdisi = st.sidebar.text_input("Matematiksel fonksiyonunuzu yazın:", "cos(x)")
    duzeltilmis_metin = kullanici_girdisi
    duzeltilmis_metin = re.sub(r'(?<!np\.)\b(sin|cos|tan|exp|sqrt|log|pi|abs)\b', r'np.\1', duzeltilmis_metin)
    duzeltilmis_metin = duzeltilmis_metin.replace("^", "**")
    
    if duzeltilmis_metin != kullanici_girdisi:
        st.sidebar.markdown(f"""
        <div style='background-color: #ffffff; padding: 10px; border-radius: 6px; border-left: 3px solid #a3b899; border-top: 1px solid #e3dec9; border-right: 1px solid #e3dec9; border-bottom: 1px solid #e3dec9;'>
            <span style='color: #556b4f;'>💡 <b>Asistan Notu:</b></span><br>
            Formülünüz arka planda yumuşakça <code>{duzeltilmis_metin}</code> haline getirildi.
        </div>
        """, unsafe_allow_html=True)
    fonksiyon_metni = duzeltilmis_metin
else:
    fonksiyon_metni = hazir_fonksiyonlar[secilen_hazir]
    st.sidebar.markdown(f"<small style='color: #7f8c8d;'>Aktif Formül: <code>{fonksiyon_metni}</code></small>", unsafe_allow_html=True)

try:
    f = lambda x: eval(fonksiyon_metni, {"np": np, "x": x})
    f(1.0)
except:
    st.sidebar.error("⚠️ İfade anlaşılamadı. Varsayılan x^2 yüklendi.")
    f = lambda x: x**2
    fonksiyon_metni = "x**2"

a = st.sidebar.number_input("İntegral Alt Sınırı (a):", value=0.0)
b = st.sidebar.number_input("İntegral Üst Sınırı (b):", value=float(np.pi if "sin" in fonksiyon_metni or "cos" in fonksiyon_metni else 2.0))
n = st.sidebar.slider("Görselleştirme Bölme Sayısı (n):", min_value=4, max_value=100, value=12)

def gelismis_hesaplayici(f, a, b, n):
    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    sol = np.sum(f(x[:-1])) * dx
    sag = np.sum(f(x[1:])) * dx
    orta = np.sum(f((x[:-1] + x[1:]) / 2)) * dx
    yamuk = (f(a) + f(b) + 2 * np.sum(f(x[1:-1]))) * (dx / 2)
    return sol, sag, orta, yamuk

try:
    gercek_deger, _ = quad(f, a, b)
except:
    gercek_deger = 0.0

sol, sag, orta, yamuk = gelismis_hesaplayici(f, a, b, n)

hatalar_anlik = {
    "Sol Riemann": abs(gercek_deger - sol),
    "Sağ Riemann": abs(gercek_deger - sag),
    "Orta Nokta": abs(gercek_deger - orta),
    "Yamuk Yöntemi": abs(gercek_deger - yamuk)
}
sampiyon = min(hatalar_anlik, key=hatalar_anlik.get)

st.markdown(f"""
<div style='background-color: #ffffff; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #e3dec9; box-shadow: 0 1px 3px rgba(0,0,0,0.02);'>
    ✨ <b>Aktif İfade:</b> <span style='color: #4a7c59;'>f(x) = {fonksiyon_metni}</span> | 
    🏆 <b>Optimum Yaklaşım:</b> <span style='color: #68809a;'>{sampiyon}</span> (Hata: {hatalar_anlik[sampiyon]:.8f})
</div>
""", unsafe_allow_html=True)
st.write("")

# ==========================================================
# 📊 3. SEKME YAPILARI VE SOFT MATPLOTLIB GÖRSELLERİ
# ==========================================================
sekme1, sekme2, sekme3 = st.tabs(["📈 İnteraktif Geometri", "📊 Asimptotik Hata Analizi", "🧠 Analiz Notları & Perde Arkası"])

with sekme1:
    st.subheader("✨ Alan Analizi ve Geometrik Yaklaşım")
    
    plt.style.use('default')
    fig, ax = plt.subplots(1, 4, figsize=(22, 4.5))
    fig.patch.set_facecolor('#f7f6f2') 
    
    x_cizim = np.linspace(a, b, 1000)
    x_blok = np.linspace(a, b, n + 1)
    dx = (b - a) / n
    
    yontemler = [
        {"ad": "Sol Riemann", "val": sol, "color": "#b2c4db"},  
        {"ad": "Sağ Riemann", "val": sag, "color": "#a3b899"},  
        {"ad": "Orta Nokta", "val": orta, "color": "#cbb2db"},  
        {"ad": "Yamuk Yöntemi", "val": yamuk, "color": "#e0c19e"} 
    ]
    
    for i, ynt in enumerate(yontemler):
        ax[i].set_facecolor('#ffffff') 
        ax[i].plot(x_cizim, f(x_cizim), '#cca4a4', linewidth=2) 
        ax[i].set_title(f"{ynt['ad']}\n(Değer: {ynt['val']:.4f})", color='#2c3e50', fontsize=11)
        ax[i].grid(True, alpha=0.2, color='#b0b0b0')
        
        if i == 0:
            ax[i].bar(x_blok[:-1], f(x_blok[:-1]), width=dx, align='edge', alpha=0.4, edgecolor=ynt['color'], color=ynt['color'])
        elif i == 1:
            ax[i].bar(x_blok[:-1] + dx, f(x_blok[1:]), width=dx, align='edge', alpha=0.4, edgecolor=ynt['color'], color=ynt['color'])
        elif i == 2:
            ax[i].bar((x_blok[:-1] + x_blok[1:])/2, f((x_blok[:-1] + x_blok[1:])/2), width=dx, align='center', alpha=0.4, edgecolor=ynt['color'], color=ynt['color'])
        elif i == 3:
            for j in range(n):
                ax[i].fill_between([x_blok[j], x_blok[j+1]], [0, 0], [f(x_blok[j]), f(x_blok[j+1])], alpha=0.4, edgecolor=ynt['color'], color=ynt['color'])

    st.pyplot(fig)
    
    st.markdown(f"<h4>🎯 Analitik Gerçek Değer (SciPy): <span style='color: #68809a;'>{gercek_deger:.6f}</span></h4>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sol Riemann Hatası", f"{hatalar_anlik['Sol Riemann']:.5f}")
    col2.metric("Sağ Riemann Hatası", f"{hatalar_anlik['Sağ Riemann']:.5f}")
    col3.metric("Orta Nokta Hatası", f"{hatalar_anlik['Orta Nokta']:.5f}")
    col4.metric("Yamuk Hatası", f"{hatalar_anlik['Yamuk Yöntemi']:.5f}")

with sekme2:
    st.subheader("📉 Çözünürlük ve Asimptotik Yakınsama Notları")
    
    st.markdown("""
    <div class="trivia-card">
        <h4 style='margin-top:0; color:#2c3e50;'>🔍 Asimptotun Mantığı Nedir?</h4>
        Analizde <b>asimptotik davranış</b>, bir sistemin girdileri veya parametreleri sınıra (burada sonsuza) doğru yaklaşırken sergilediği nihai eğilimdir. 
        Aşağıdaki logaritmik grafikte, alt bölme sayısı (n) arttıkça hata oranlarının pürüzsüz doğrular halinde aşağı indiğini görüyorsunuz.
        <br><br>
        Buradaki matematiksel asır şudur: Dikdörtgen sayısı (n) sonsuza doğru koştukça, her bir yöntemin hata fonksiyonu sıfır doğrusuna <b>asimptotik olarak yaklaşır</b>. Hata hiçbir zaman mutlak olarak sonsuz adımlı bilgisayarda tam sıfır olmaz (çünkü her zaman minik bir yuvarlama hatası kalır), ancak hatanın limiti sıfırdır. Bu grafikteki doğruların eğimleri ise bize yöntemlerin yakınsama hızını (O(1/n) veya O(1/n²)) gösterir.
    </div>
    """, unsafe_allow_html=True)
    
    n_listesi = [10, 25, 50, 100, 250, 500, 1000]
    h_sol, h_sag, h_orta, h_yamuk = [], [], [], []
    
    for n_t in n_listesi:
        s, sg, o, y = gelismis_hesaplayici(f, a, b, n_t)
        h_sol.append(abs(gercek_deger - s))
        h_sag.append(abs(gercek_deger - sg))
        h_orta.append(abs(gercek_deger - o))
        h_yamuk.append(abs(gercek_deger - y))
        
    fig_hata, ax_hata = plt.subplots(figsize=(11, 3.5))
    fig_hata.patch.set_facecolor('#f7f6f2')
    ax_hata.set_facecolor('#ffffff')
    
    ax_hata.loglog(n_listesi, h_sol, '-o', color="#b2c4db", label="Sol Hata")
    ax_hata.loglog(n_listesi, h_sag, '-s', color="#a3b899", label="Sağ Hata")
    ax_hata.loglog(n_listesi, h_orta, '-^', color="#cbb2db", label="Orta Nokta Hata")
    ax_hata.loglog(n_listesi, h_yamuk, '-d', color="#e0c19e", label="Yamuk Hata")
    ax_hata.set_xlabel("Alt Bölme Sayısı (n)", color='#2c3e50')
    ax_hata.set_ylabel("Hata Oranı", color='#2c3e50')
    ax_hata.grid(True, which="both", ls="--", alpha=0.2, color='#b0b0b0')
    ax_hata.legend(facecolor='#ffffff', edgecolor='#e3dec9')
    st.pyplot(fig_hata)
    
    df = pd.DataFrame({
        "n Bölme": n_listesi,
        "Sol Riemann": h_sol, "Sağ Riemann": h_sag, "Orta Nokta": h_orta, "Yamuk Yöntemi": h_yamuk
    })
    st.dataframe(df.style.highlight_min(axis=1, color='#e2ece9').format({c: "{:.8f}" for c in df.columns if c != "n Bölme"}))

with sekme3:
    st.markdown("## 🧠 Kalkülüsün Derinlikleri: Limit ve Sonsuzluk")
    st.write("---")
    
    st.markdown(f"""
    <div class="ai-card">
        <h3 style='color: #556b4f !important; margin-top:0;'>🔍 Fonksiyonel Analiz: Ayrık Dünyadan Sürekli Evrene</h3>
        Laboratuvarda seçtiğiniz fonksiyonda kesit sayılarını artırdıkça hataların nasıl sıfıra çöktüğünü gördünüz.<br><br>
        Burada yaptığınız işlem, bilgisayarın işlemcisinde dönen ayrık (discrete) toplama algoritmalarını, limit yardımıyla doğanın dili olan sürekli (continuous) bir integrale dönüştürmektir. Dikdörtgenlerin genişliği sıfıra yaklaşırken Riemann Toplamı, o meşhur analitik integral alanına evrilir:
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r"\makeatletter \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i) \Delta x = \int_{a}^{b} f(x) dx \makeatother")
    
    st.markdown("""
    <div class="trivia-card">
        <h3 style='color: #4a6b82 !important; margin-top:0;'>💡 Biliyor muydunuz? (Kalkülüs Savaşları)</h3>
        Bugün Riemann'ın geometrik olarak modernize ettiği bu entegrasyon metodunun temelleri, 17. yüzyılda <b>Isaac Newton</b> ve <b>Gottfried Wilhelm Leibniz</b> tarafından birbirlerinden tamamen bağımsız olarak aynı dönemde keşfedildi.<br><br>
        Newton calculus'ü fiziksel hareketleri (akışları) açıklamak için kullanırken, Leibniz daha felsefi ve sembolik bir yaklaşımla bugünkü integral işaretini geliştirdi. İki dahi, bu keşfin mülkiyeti için bilim tarihine <b>'Kalkülüs Savaşları'</b> olarak geçen büyük bir entelektüel kavga verdiler.
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    st.markdown("""
    <div class="ouverture-card">
        <h3 style='color: #9e6b6b !important; margin-top:0;'>🧐 Ufuk Çizgisi</h3>
        <p style='font-style: italic; font-size: 1.05em; color: #5c3a3a;'>
        "Geliştirdiğimiz bu laboratuvarda gördüğümüz gibi; bilgisayarlar ve dijital sistemler doğadaki pürüzsüz ve sürekli eğrileri ancak 'sonsuz küçük parçalara/dikdörtgenlere bölerek' taklit edebilir.<br><br>
        Peki, bizim <b>Yapay Zeka (AI)</b> modellerimiz de insan zihninin pürüzsüz, sezgisel ve sürekli düşünme biçimini sadece milyarlarca 'ayrık' veri noktasını ve matrisi alt alta toplayıp olasılık hesaplayarak simüle ediyorsa; yapay zeka hiçbir zaman gerçek anlamda 'kesintisiz bir bilince' ulaşamayacak, sadece mükemmel dikdörtgenler çizen harika bir illüzyon olarak mı kalacaktır? Yoksa insan beyni de aslında verileri sadece bu şekilde ayrık dalgalar halinde mi işliyor?"
        </p>
    </div>
    """, unsafe_allow_html=True)