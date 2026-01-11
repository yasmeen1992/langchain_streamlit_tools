# langchain_streamlit_tools

واجهة Streamlit بسيطة لأسئلة وأجوبة مدعومة بأدوات ومكونات مساعدة (LangChain).

الملفات الرئيسية
- `ui.py` — واجهة المستخدم المبنية بـ Streamlit.
- `chat_agent.py` — منطق وكاتب الوكلاء ونقاط الدخول الخلفية.
- `tools.py` — أدوات مساعدة ومكونات قابلة لإعادة الاستخدام.

التثبيت
1. أنشئ بيئة افتراضية (موصى به):

```bash
python -m venv .venv
.
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

2. ثبّت المتطلبات:

```bash
pip install -r requirements.txt
```

التشغيل

لتشغيل واجهة Streamlit محليًا:

```bash
streamlit run ui.py
```

أو لاختبار مكوّن الوكيل مباشرة:

```bash
python chat_agent.py
```

ملاحظات
- راجع `requirements.txt` لتحديث الحزم أو إضافة متطلبات جديدة.
- أخبرني إذا رغبت أن أضيف أمثلة استخدام أو صور شاشة للواجهة.