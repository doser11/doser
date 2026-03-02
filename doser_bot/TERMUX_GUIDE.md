# 📱 Termux Installation & Usage Guide

دليل تشغيل Doser على Termux (Android)

---

## ⚠️ متطلبات الجهاز

- **Android 7.0+** (API 24)
- **ذاكرة RAM**: 2GB على الأقل
- **مساحة تخزين**: 500MB فارغة
- **إنترنت** مستقر

---

## 📥 تثبيت Termux

### من F-Droid (موصى به)

1. حمل Termux من [F-Droid](https://f-droid.org/packages/com.termux/)
2. **لا تحمل من Google Play** (نسخة قديمة)

### أو مباشرة

```bash
# تحميل APK
wget https://f-droid.org/repo/com.termux_118.apk
```

---

## 🔧 خطوات التثبيت

### 1. تحديث الحزم

```bash
pkg update && pkg upgrade -y
```

### 2. تثبيت Python و Git

```bash
pkg install python git -y
```

### 3. تثبيت Chrome/Chromium

```bash
pkg install chromium -y
```

أو:

```bash
pkg install x11-repo -y
pkg install tur-repo -y
pkg install chromium-browser -y
```

### 4. تثبيت مكتبات إضافية

```bash
pkg install libxml2 libxslt libffi openssl -y
```

### 5. تحميل Doser

```bash
cd ~
git clone https://github.com/yourusername/doser.git
# أو انسخ الملفات يدوياً
```

### 6. تثبيت المتطلبات

```bash
cd doser
pip install -r requirements.txt
```

---

## 🚀 التشغيل

### الوضع التفاعلي (CLI)

```bash
cd ~/doser
python cli.py
```

### سريع مباشر

```bash
cd ~/doser
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 1
```

### مع بروكسي ومتابعة

```bash
cd ~/doser
python cli.py \
  --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" \
  --count 3 \
  --proxy-file proxies.txt \
  --follow "target_username"
```

---

## 📋 أوامر سريعة

```bash
# الدخول للمجلد
cd ~/doser

# تشغيل CLI
python cli.py

# تشغيل GUI (إذا كان متاح X11)
python main.py

# اختبار البوت
python -c "from core.email_bot import EmailBot; bot = EmailBot('8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU'); print('✅ OK' if bot.test_connection() else '❌ Failed')"

# عرض الحسابات المنشأة
cat accounts/accounts.json

# تحرير الإعدادات
nano .env
```

---

## 🐛 حل المشاكل الشائعة

### مشكلة: `pip install` يفشل

```bash
# حل
pkg install python-pip -y
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### مشكلة: `chromium` غير موجود

```bash
# حل
pkg install x11-repo -y
pkg install chromium -y
# أو
pkg install termux-chromium -y
```

### مشكلة: `No module named '_ctypes'`

```bash
# حل
pkg install libffi -y
pip install cffi
```

### مشكلة: الذاكرة غير كافية

```bash
# حل: أغلق التطبيقات الأخرى
# أو استخدم وضع Headless
python cli.py --headless --token "TOKEN" --count 1
```

### مشكلة: الخروج المفاجئ

```bash
# حل: شغل في screen
pkg install screen -y
screen -S doser
python cli.py
# للخروج: Ctrl+A ثم D
# للعودة: screen -r doser
```

---

## 🔄 تشغيل مستمر (Background)

```bash
# تثبيت screen
pkg install screen -y

# إنشاء جلسة جديدة
screen -S doser

# تشغيل الأداة
cd ~/doser
python cli.py --token "8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU" --count 5

# فصل الجلسة: Ctrl+A ثم D

# العودة للجلسة
screen -r doser

# قائمة الجلسات
screen -ls
```

---

## 📱 نصائح Termux

### حفظ البيانات

```bash
# نسخ احتياطي
termux-setup-storage
cp -r ~/doser /sdcard/Download/doser_backup

# استعادة
cp -r /sdcard/Download/doser_backup ~/doser
```

### منع إيقاف Termux

```bash
# قفل التطبيق في الذاكرة (Android)
# Settings > Battery > Battery Optimization > All Apps > Termux > Don't Optimize
```

### تشغيل بدون إنترنت

```bash
# لا يمكن - يحتاج إنترنت للبوت وإنستغرام
```

---

## 🎯 سكربت تشغيل سريع

أنشئ ملف `run.sh`:

```bash
#!/data/data/com.termux/files/usr/bin/bash

cd ~/doser

echo "╔═══════════════════════════════════════╗"
echo "║     💉 DOSER - Termux Edition 💉     ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# التحقق من التوكن
TOKEN="8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU"

echo "🔑 Bot Token: ${TOKEN:0:20}..."
echo ""

# عدد الحسابات
read -p "📊 Number of accounts [1]: " count
count=${count:-1}

# متابعة حساب
read -p "👤 Account to follow (optional): " follow

# تشغيل
echo ""
echo "🚀 Starting..."
echo ""

if [ -z "$follow" ]; then
    python cli.py --token "$TOKEN" --count "$count"
else
    python cli.py --token "$TOKEN" --count "$count" --follow "$follow"
fi
```

اجعله قابل للتنفيذ:

```bash
chmod +x run.sh
./run.sh
```

---

## 📊 مراقبة الأداء

```bash
# مراقبة الموارد
htop

# مساحة التخزين
df -h

# استخدام الذاكرة
free -m
```

---

## 🧹 تنظيف

```bash
# حذف الكاش
pip cache purge

# حذف السجلات القديمة
rm -rf logs/*

# حذف الحسابات (احتفظ بنسخة!)
rm -rf accounts/*
```

---

## 📞 دعم Termux

- [Termux Wiki](https://wiki.termux.com/)
- [Termux GitHub](https://github.com/termux/termux-app)
- Telegram: @termux_group

---

**✅ جاهز للتشغيل على Termux!**
