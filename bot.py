import time, warnings, requests, yfinance as yf
warnings.filterwarnings("ignore")

TOKEN = '8461456577:AAEjzZRgoJOpvkh7tbQnuIN1JsHjw2VST2U'
CHAT_ID = '1097510014'

STOCKS = {
    # الدفعة الأولى والثانية (المجموعة السابقة)
    'COMI.CA':'التجاري الدولي','HRHO.CA':'إي إف جي','BTFH.CA':'بلتون',
    'TMGH.CA':'طلعت مصطفى','PALM.CA':'بالم هيلز','MNHD.CA':'مدينة مصر',
    'ABUK.CA':'أبو قير','MFPC.CA':'موبكو','SKPC.CA':'سيدي كرير','AMOC.CA':'أموك',
    'ESRS.CA':'حديد عز','EGAL.CA':'مصر للألومنيوم','SWDY.CA':'السويدي',
    'JUFO.CA':'جهينة','DOMT.CA':'دومتي','EAST.CA':'إيسترن كومباني',
    'FWRY.CA':'فوري','EFIH.CA':'إي فاينانس','ETEL.CA':'المصرية للاتصالات',
    'OCDI.CA':'سوديك','HELI.CA':'مصر الجديدة','PHDC.CA':'المطورون العرب',
    'RMDA.CA':'رميدا','ISPH.CA':'ابن سينا','CLHO.CA':'كليوباترا',
    'CSAG.CA':'القناة للتوكيلات','ALCN.CA':'الإسكندرية للحاويات',
    'ORWE.CA':'النساجون الشرقيون','KABO.CA':'كابو','EGTS.CA':'المنتجعات',
    
    # الدفعة الجديدة المضافة
    'ADIB.CA':'أبوظبي الإسلامي','CIEB.CA':'كريدي أجريكول','HDBK.CA':'التعمير والإسكان',
    'QNBA.CA':'قطر الوطني','AUTO.CA':'أوتو كابيتال','RAYA.CA':'راية القابضة',
    'ORAS.CA':'أوراسكوم كونستراكشون','EKHO.CA':'المصرية الكويتية','ARCC.CA':'العربية للأسمنت',
    'SPMD.CA':'سبيد ميديكال','AJWA.CA':'اجواء','DDBP.CA':'دلتا للسكر',
    'RTVC.CA':'رمكو للقرى','MHOT.CA':'مصر للفنادق','CCRS.CA':'سي آي كابيتال'
}

def send(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except: pass

for t, n in STOCKS.items():
    try:
        df = yf.download(t, period='1mo', interval='1d', progress=False)
        if not df.empty and len(df) >= 20:
            d = df['Close'].diff()
            g = d.where(d > 0, 0).rolling(14).mean()
            l = (-d.where(d < 0, 0)).rolling(14).mean()
            rsi = float((100 - (100 / (1 + (g / l)))).values[-1])
            p = float(df['Close'].values[-1])
            if rsi < 58:
                send(f"🟢 <b>[فرصة شراء]</b>\n📈 <b>السهم:</b> {n} (<code>{t}</code>)\n💰 <b>السعر:</b> {p:.2f} ج.م\n🎯 <b>الهدف (+4%):</b> {p*1.04:.2f} ج.م\n🚨 <b>وقف الخسارة:</b> {p*0.98:.2f} ج.م\n📊 <b>RSI:</b> {rsi:.1f}")
                time.sleep(0.1)
    except: pass
