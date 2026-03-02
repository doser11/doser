# 🚀 Quick Start - Termux

## ⚡ خطوات سريعة للتشغيل

### 1️⃣ تثبيت Termux
- حمل Termux من [F-Droid](https://f-droid.org/packages/com.termux/)
- **لا تحمل من Google Play**

### 2️⃣ نسخ ولصق هذه الأوامر بالترتيب:

```bash
# 1. تحديث الحزم
pkg update && pkg upgrade -y

# 2. تثبيت Python و Git
pkg install python git -y

# 3. تثبيت Chromium
pkg install x11-repo -y
pkg install chromium -y

# 4. تحميل المشروع
cd ~
git clone https://github.com/yourusername/doser.git

# أو إذا عندك الملفات محلياً:
# cp -r /path/to/doser ~/

# 5. دخول المجلد
cd doser

# 6. تثبيت المتطلبات
pip install -r requirements.txt

# 7. تشغيل!
python cli.py
```

---

## 🎯 التشغيل السريع

### الطريقة 1: Interactive (موصى بها للمبتدئين)

```bash
cd ~/doser
python cli.py
```

ثم اتبع التعليمات التي تظهر.

### الطريقة 2: سريع مباشر

```bash
cd ~/doser
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 1
```

### الطريقة 3: باستخدام السكربت الجاهز

```bash
cd ~/doser
chmod +x termux_run.sh
./termux_run.sh
```

ثم اختر رقم من القائمة.

---

## 📋 أوامر مفيدة

| الأمر | الوظيفة |
|-------|---------|
| `cd ~/doser` | دخول مجلد المشروع |
| `python cli.py` | تشغيل الوضع التفاعلي |
| `python cli.py --count 5` | إنشاء 5 حسابات |
| `cat accounts/accounts.json` | عرض الحسابات المنشأة |
| `nano .env` | تعديل الإعدادات |
| `nano proxies.txt` | تعديل البروكسيات |

---

## ⚙️ أمثلة للتشغيل

### إنشاء حساب واحد:
```bash
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 1
```

### إنشاء 5 حسابات:
```bash
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 5
```

### إنشاء ومتابعة حساب:
```bash
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 3 --follow "cristiano"
```

### مع بروكسي:
```bash
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 2 --proxy-file proxies.txt
```

### وضع Headless (بدون متصفح مرئي):
```bash
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 1 --headless
```

---

## 🔄 خطوات العمل

1. **شغل الأداة** بأي طريقة من الطرق أعلاه
2. **انتظر** فتح المتصفح
3. **انتظر** وصول رمز التحقق إلى بوتك على Telegram
4. **الأداة تدخل الرمز تلقائياً**
5. **تكمل بيانات الحساب**
6. **تحفظ الحساب** في ملف `accounts/accounts.json`

---

## 📁 أين تجد النتائج؟

```
~/doser/accounts/accounts.json    # الحسابات المنشأة
~/doser/logs/doser.log            # السجلات
~/doser/proxies.txt               # قائمة البروكسيات
```

---

## 🛠️ حل المشاكل

### مشكلة: "command not found"
```bash
pkg install python -y
```

### مشكلة: "No module named..."
```bash
pip install -r requirements.txt
```

### مشكلة: "chromedriver not found"
```bash
pkg install chromium -y
```

### مشكلة: الخروج المفاجئ
```bash
pkg install screen -y
screen -S doser
python cli.py
# اضغط Ctrl+A ثم D للخروج بدون إيقاف
```

---

## 📞 للمساعدة

- افتح تطبيق Telegram
- ابحث عن بوتك باستخدام التوكن
- تأكد من إرسال `/start` للبوت

---

**✨ جاهز للاستخدام!**
