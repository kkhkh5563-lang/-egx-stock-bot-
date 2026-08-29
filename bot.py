import os, time, warnings, requests, yfinance as yf
warnings.filterwarnings("ignore")

TOKEN = '8461456577:AAEjzZRgoJOpvkh7tbQnuIN1JsHjw2VST2U'
CHAT_ID = '1097510014'

STOCKS = {
    'COMI.CA': 'التجاري الدولي',
    'HRHO.CA': 'إي إف جي القابضة',
    'FWRY.CA': 'فوري',
    'BTFH.CA': 'بلتون القابضة',
    'ADIB.CA': 'أبوظبي الإسلامي',
    'CIEB.CA': 'كريدي أجريكول',
    'EFIH.CA': 'إي فاينانس',
    'BINV.CA': 'بي إنفستمنتس',
    'HDBK.CA': 'بنك التعمير والإسكان',
    'EGBE.CA': 'البنك المصري الخليجي',
    'FAIT.CA': 'فيصل الإسلامي',
    'TMGH.CA': 'طلعت مصطفى',
    'PALM.CA': 'بالم هيلز',
    'MNHD.CA': 'مدينة مصر',
    'HELI.CA': 'مصر الجديدة للإسكان',
    'OCDI.CA': 'سوديك',
    'ORHD.CA': 'أوراسكوم للتنمية',
    'UEGC.CA': 'إعمار مصر',
    'PHDC.CA': 'المطورون العرب',
    'ZMID.CA': 'زهراء المعادي',
    'ELSH.CA': 'الشمس للإسكان',
    'ORAS.CA': 'أوراسكوم كونستراكشون',
    'ARAB.CA': 'عربية أصول',
    'PRDC.CA': 'بايونيرز بروبرتيز',
    'ABUK.CA': 'أبو قير للأسمدة',
    'MFPC.CA': 'موبكو',
    'SKPC.CA': 'سيدي كرير',
    'AMOC.CA': 'أموك',
    'EKHO.CA': 'المصرية الكويتية',
    'ESRS.CA': 'حديد عز',
    'EGAL.CA': 'مصر للألومنيوم',
    'SWDY.CA': 'السويدي إليكتريك',
    'DDBP.CA': 'دلتا للسكر',
    'ARCC.CA': 'العربية لأسمنت',
    'SVCE.CA': 'جنوب الوادي لأسمنت',
    'MCQE.CA': 'مصر بني سويف لأسمنت',
    'RMDA.CA': 'رميدا',
    'ISPH.CA': 'ابن سينا فارما',
    'CLHO.CA': 'كليوباترا',
    'SPMD.CA': 'سبيد ميديكال',
    'MOPH.CA': 'ممفيس للأدوية',
    'CPCI.CA': 'القاهرة للأدوية',
    'NIPH.CA': 'النيل للأدوية',
    'AIND.CA': 'العربية للاستثمار',
    'GDWA.CA': 'جدوى للإستثمار',
    'ODIN.CA': 'أودن للاستثمار',
    'RAYA.CA': 'راية القابضة',
    'AUTO.CA': 'أوتو كابيتال',
    'GBCO.CA': 'جي بي كورب',
    'RTVC.CA': 'رمكو لإنشاء القرى',
    'EGTS.CA': 'المنتجعات السياحية',
    'ISSC.CA': 'الشرقية الوطنية',
    'CCTC.CA': 'القاهرة للزيوت',
    'KABO.CA': 'كابو',
    'ACGC.CA': 'العربية لحجيج القطن',
    'CSAG.CA': 'القناة للتوكيلات',
    'ALCN.CA': 'الإسكندرية للحاويات',
    'ETEL.CA': 'المصرية للاتصالات',
    'EAST.CA': 'إيسترن كومباني',
    'JUFO.CA': 'جهينة',
    'DOMT.CA': 'دومتي',
    'ORWE.CA': 'النساجون الشرقيون',
    'AJWA.CA': 'اجواء',
    'ATQA.CA': 'مصر الوطنية للصلب',
    'OIH.CA': 'أوراسكوم للاستثمار',
    'DAPH.CA': 'مستشفى النزهة',
    'ZEOT.CA': 'الزيوت المستخلصة'
}

def send(msg):
    try:
        requests.post(
            f'https://api.telegram.org/bot{TOKEN}/sendMessage',
            json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'},
            timeout=10
        )
    except:
        pass

for t, n in STOCKS.items():
    try:
        df = yf.download(t, period='1mo', interval='1d', progress=False)
        if not df.empty and len(df) >= 20:
            d = df['Close'].diff()
            g = d.where(d > 0, 0).rolling(14).mean()
            l = (-d.where(d < 0, 0)).rolling(14).mean()
            rsi_val = (100 - (100 / (1 + (g / l)))).values[-1]
            rsi = float(rsi_val.item() if hasattr(rsi_val, 'item') else rsi_val)

            p_val = df['Close'].values[-1]
            p = float(p_val.item() if hasattr(p_val, 'item') else p_val)

            if rsi < 58:
                target_price = p * 1.04
                stop_loss = p * 0.98
                msg = (
                    f"🟢 <b>[فرصة شراء ومضاربة]</b>\n"
                    f"📈 <b>السهم:</b> {n} (<code>{t}</code>)\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 <b>سعر الشراء الحالي:</b> {p:.2f} ج.م\n"
                    f"🎯 <b>الهدف المتوقع (+4.0%):</b> {target_price:.2f} ج.م\n"
                    f"🚨 <b>وقف الخسارة الصارم:</b> {stop_loss:.2f} ج.م\n"
                    f"📊 <b>مؤشر RSI:</b> {rsi:.1f}\n"
                    f"💡 <b>التوصية:</b> دخول وتجهيز أهداف الربح."
                )
                send(msg)
                time.sleep(0.1)
    except:
        pass
