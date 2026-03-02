# 📦 Doser Installation Guide

دليل التثبيت الكامل لأداة Doser

## 🖥️ المتطلبات الأساسية

- **Python 3.8** أو أحدث
- **Google Chrome** متصفح
- **Windows 10/11** أو **Linux** أو **macOS**

---

## 🚀 التثبيت السريع

### Windows

1. **تحميل المشروع:**
```bash
git clone https://github.com/yourusername/doser.git
cd doser
```

2. **تشغيل سكريبت التثبيت:**
```bash
install.bat
```

أو يدوياً:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **التشغيل:**
```bash
start.bat
```

---

### Linux / macOS

1. **تحميل المشروع:**
```bash
git clone https://github.com/yourusername/doser.git
cd doser
```

2. **تثبيت المتطلبات:**
```bash
chmod +x install.sh start.sh
./install.sh
```

أو يدوياً:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **التشغيل:**
```bash
./start.sh
```

---

## 🔧 التثبيت اليدوي

### 1. تثبيت Python

**Windows:**
- حمل Python من [python.org](https://python.org)
- تأكد من تحديد "Add Python to PATH"

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

### 2. تثبيت Chrome

**Windows:**
- حمل Chrome من [google.com/chrome](https://google.com/chrome)

**Linux:**
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt update
sudo apt install google-chrome-stable
```

**macOS:**
```bash
brew install --cask google-chrome
```

### 3. إعداد المشروع

```bash
# إنشاء مجلد المشروع
mkdir doser
cd doser

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt
```

---

## ⚙️ الإعداد الأولي

### 1. إنشاء بوت Telegram

1. افتح Telegram وابحث عن **@BotFather**
2. أرسل الأمر `/newbot`
3. اتبع التعليمات:
   - أدخل اسم للبوت (مثال: `MyDoserBot`)
   - أدخل معرف للبوت (يجب أن ينتهي بـ `bot`, مثال: `mydoser_bot`)
4. **احفظ التوكن** الذي سيعطيه لك

### 2. الحصول على Chat ID

1. ابحث عن **@userinfobot** في Telegram
2. ابدأ المحادثة
3. سيعطيك معرفك (Chat ID)

### 3. إعداد ملف البيئة

```bash
# نسخ ملف المثال
cp .env.example .env

# تعديل الملف
nano .env  # أو استخدم أي محرر
```

أضف معلوماتك:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. إعداد البروكسي (اختياري)

```bash
# نسخ ملف المثال
cp proxies.txt.example proxies.txt

# تعديل الملف
nano proxies.txt
```

أضف بروكسياتك:
```
http://user:pass@192.168.1.1:8080
socks5://192.168.1.2:1080
https://proxy.example.com:3128
```

---

## 🧪 اختبار التثبيت

```bash
# اختبار المكونات
python test_bot.py

# اختبار الاتصال بالبوت
python -c "
from core.email_bot import EmailBot
import os
from dotenv import load_dotenv
load_dotenv()

bot = EmailBot(os.getenv('TELEGRAM_BOT_TOKEN'))
print('✅ Connected!' if bot.test_connection() else '❌ Failed')
"
```

---

## 🎮 الاستخدام

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

---

## 🔧 حل المشاكل

### مشكلة: `ModuleNotFoundError`

**الحل:**
```bash
pip install -r requirements.txt
```

### مشكلة: `chromedriver` غير موجود

**الحل:**
```bash
pip install --upgrade webdriver-manager
```

### مشكلة: البوت لا يستجيب

**التحقق:**
1. تأكد من صحة التوكن
2. تأكد من إرسال رسالة للبوت أولاً
3. تأكد من صحة Chat ID

```bash
# اختبار البوت
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### مشكلة: البروكسي لا يعمل

**التحقق:**
```bash
# اختبار البروكسي
curl -x http://user:pass@ip:port https://httpbin.org/ip
```

---

## 📁 هيكل الملفات

بعد التثبيت:
```
doser/
├── venv/                   # البيئة الافتراضية
├── data/                   # البيانات
├── logs/                   # السجلات
├── accounts/               # الحسابات المنشأة
│   └── accounts.json
├── proxies.txt             # ملف البروكسي
├── .env                    # إعدادات البيئة
├── main.py                 # الملف الرئيسي
└── requirements.txt        # المتطلبات
```

---

## 🔄 التحديث

```bash
# سحب التحديثات
git pull

# تحديث المكتبات
pip install -r requirements.txt --upgrade
```

---

## ❌ إلغاء التثبيت

```bash
# حذف البيئة الافتراضية
rm -rf venv/

# حذف ملفات البيانات
rm -rf data/ logs/ accounts/

# حذف الإعدادات
rm .env proxies.txt
```

---

## 📞 الدعم

للمساعدة:
- Telegram: @your_support
- GitHub Issues: [github.com/yourusername/doser/issues](https://github.com/yourusername/doser/issues)

---

**✨ تم التثبيت بنجاح! جرب تشغيل البرنامج الآن.**
