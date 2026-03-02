# 💉 Doser - Instagram Account Creator

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>أداة متقدمة لإنشاء حسابات إنستغرام تلقائياً</b>
</p>

<p align="center">
  <a href="#-المميزات">المميزات</a> •
  <a href="#-التثبيت">التثبيت</a> •
  <a href="#-الاستخدام">الاستخدام</a> •
  <a href="#-التوثيق">التوثيق</a> •
  <a href="#-الدعم">الدعم</a>
</p>

---

## ✨ المميزات

- 🎨 **واجهة رسومية حديثة** - تصميم جميل باستخدام CustomTkinter
- 🤖 **أتمتة كاملة** - إنشاء حسابات تلقائياً مع التعامل مع التحقق
- 📧 **دعم البوت** - استقبال رموز التحقق عبر Telegram Bot
- 🔄 **تدوير البروكسي** - تغيير IP تلقائياً لكل حساب
- 🔍 **فحص اليوزرات** - التحقق من توفر أسماء المستخدمين
- 👥 **متابعة تلقائية** - متابعة حساب معين بعد الإنشاء
- 🔒 **كلمة سر موحدة** - P@ssword81297 لجميع الحسابات
- 📊 **إحصائيات** - تتبع الحسابات المنشأة
- 💾 **تصدير متعدد** - TXT, CSV, JSON

---

## 📸 Screenshots

<p align="center">
  <i>واجهة المستخدم الرسومية</i>
</p>

---

## 🚀 التثبيت

### سريع (Windows)

```bash
git clone https://github.com/yourusername/doser.git
cd doser
install.bat
start.bat
```

### سريع (Linux/macOS)

```bash
git clone https://github.com/yourusername/doser.git
cd doser
chmod +x install.sh start.sh
./install.sh
./start.sh
```

### يدوي

```bash
# Clone repository
git clone https://github.com/yourusername/doser.git
cd doser

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

📖 [دليل التثبيت الكامل](INSTALL.md)

---

## 💻 الاستخدام

### الوضع الرسومي (GUI)

```bash
python main.py
```

### الوضع التفاعلي (CLI)

```bash
python cli.py
```

### سريع مع معاملات

```bash
python cli.py --token "YOUR_TOKEN" --count 5 --proxy proxies.txt
```

📖 [دليل الاستخدام الكامل](USAGE.md)

---

## ⚙️ الإعداد

### 1. إنشاء بوت Telegram

1. افتح Telegram وابحث عن **@BotFather**
2. أرسل `/newbot` واتبع التعليمات
3. احفظ **Bot Token**

### 2. الحصول على Chat ID

ابحث عن **@userinfobot** في Telegram

### 3. إعداد ملف .env

```bash
cp .env.example .env
# Edit .env with your credentials
```

---

## 📁 هيكل المشروع

```
doser/
├── config/              # الإعدادات
├── core/                # المنطق الرئيسي
│   ├── instagram_automation.py
│   ├── email_bot.py
│   └── instagram_signup_flow.py
├── gui/                 # الواجهة الرسومية
│   ├── main_window.py
│   └── enhanced_main_window.py
├── utils/               # الأدوات المساعدة
│   ├── proxy_manager.py
│   ├── generators.py
│   ├── email_parser.py
│   └── account_manager.py
├── main.py              # نقطة الدخول
├── cli.py               # واجهة سطر الأوامر
├── requirements.txt     # المتطلبات
└── README.md           # هذا الملف
```

---

## 📚 التوثيق

- [INSTALL.md](INSTALL.md) - دليل التثبيت
- [USAGE.md](USAGE.md) - دليل الاستخدام
- [CONTRIBUTING.md](CONTRIBUTING.md) - المساهمة
- [CHANGELOG.md](CHANGELOG.md) - سجل التغييرات
- [SECURITY.md](SECURITY.md) - الأمان

---

## 🛡️ الأمان

- ✅ جميع البيانات تُحفظ محلياً
- ✅ لا يتم إرسال أي معلومات للخوادم
- ✅ دعم البروكسي للخصوصية
- ✅ تدابير مضادة للكشف

⚠️ **تنبيه**: هذا البرنامج للأغراض التعليمية فقط. استخدمه على مسؤوليتك الخاصة.

---

## 🤝 المساهمة

نرحب بالمساهمات! اقرأ [دليل المساهمة](CONTRIBUTING.md) للبدء.

1. Fork المستودع
2. أنشئ فرعاً (`git checkout -b feature/amazing`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing`)
5. افتح Pull Request

---

## 📊 إحصائيات

![GitHub stars](https://img.shields.io/github/stars/yourusername/doser?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/doser?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/doser)
![GitHub license](https://img.shields.io/github/license/yourusername/doser)

---

## 📞 الدعم

- 💬 Telegram: [@your_support](https://t.me/your_support)
- 🐛 GitHub Issues: [github.com/yourusername/doser/issues](https://github.com/yourusername/doser/issues)
- 📧 Email: support@doser.app

---

## ⭐ اعطنا نجمة

إذا أعجبك المشروع، لا تنسَ إعطائه نجمة ⭐

---

## 📄 الترخيص

هذا المشروع مرخص بموجب [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by Doser Team
</p>
