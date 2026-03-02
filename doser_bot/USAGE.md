# 📖 Doser Usage Guide

دليل الاستخدام الكامل لأداة Doser

---

## 🚀 البدء السريع

### 1. تشغيل الوضع الرسومي (GUI)

```bash
# Windows
start.bat

# Linux/macOS
./start.sh

# أو مباشرة
python main.py
```

### 2. تشغيل الوضع التفاعلي (CLI)

```bash
python cli.py
```

---

## 🎨 الوضع الرسومي (GUI)

### إنشاء حسابات

1. **افتح التبويب "🚀 Create"**

2. **أدخل الإعدادات:**
   - **Number of Accounts:** عدد الحسابات المراد إنشاؤها
   - **Telegram Bot Token:** توكن البوت
   - **Chat ID:** معرف المحادثة (اختياري)
   - **Proxy File:** ملف البروكسي (اختياري)

3. **الخيارات:**
   - ☑️ **Follow account after creation** - لمتابعة حساب بعد الإنشاء
   - ☑️ **Headless mode** - تشغيل بدون نافذة متصفح
   - ☑️ **Save accounts to file** - حفظ الحسابات تلقائياً

4. **اضغط "▶ START CREATION"**

5. **انتظر** حتى يصل رمز التحقق إلى البوت

### فحص اليوزرات

1. **افتح تبويب "🔍 Check Usernames"**
2. **أدخل العدد المطلوب**
3. **اضغط "Generate & Check"**
4. **احفظ النتائج** أو انسخها

### عرض الحسابات

1. **افتح تبويب "📋 Accounts"**
2. **ابحث** عن حساب محدد
3. **صدر** الحسابات بصيغة TXT أو CSV
4. **احذف** الحسابات غير المطلوبة

### الإحصائيات

1. **افتح تبويب "📊 Statistics"**
2. **شاهد:**
   - إجمالي الحسابات
   - الحسابات النشطة
   - الحسابات المنشأة اليوم
   - الحسابات هذا الأسبوع

---

## 💻 الوضع التفاعلي (CLI)

### الوضع التفاعلي

```bash
$ python cli.py

💉  D O S E R  -  CLI Mode  💉

📋 Configuration:

🔑 Telegram Bot Token: YOUR_BOT_TOKEN
💬 Chat ID (optional): YOUR_CHAT_ID
📊 Number of accounts [1]: 5
📁 Proxy file (optional): proxies.txt

⚙️ Advanced Options:
  👤 Follow account (optional): target_username
  👻 Headless mode [y/N]: n
  ⏱️  Min delay [30]: 30
  ⏱️  Max delay [60]: 60

📋 Summary:
  Accounts: 5
  Proxy file: proxies.txt
  Follow: target_username
  Headless: False
  Delay: 30-60s

✓ Start? [Y/n]: Y

🚀 Starting...

[==================================================] 5/5

📊 SUMMARY
  ✅ Successful: 5
  ❌ Failed: 0
  📁 Accounts saved to: accounts/accounts.json

✨ Done!
```

### الوضع السريع

```bash
# إنشاء 5 حسابات
python cli.py --token "YOUR_TOKEN" --count 5

# مع بروكسي ومتابعة
python cli.py -t "TOKEN" -n 3 -p proxies.txt -f target_user

# وضع Headless
python cli.py -t "TOKEN" -n 10 --headless
```

### توليد يوزرات

```bash
python cli.py --mode usernames --count 20
```

### تصدير الحسابات

```bash
# تصدير كـ TXT
python cli.py --mode export --format txt --output accounts.txt

# تصدير كـ CSV
python cli.py --mode export --format csv --output accounts.csv

# تصدير كـ JSON
python cli.py --mode export --format json --output accounts.json
```

---

## 🤖 إعداد Telegram Bot

### 1. إنشاء البوت

1. افتح Telegram
2. ابحث عن **@BotFather**
3. أرسل `/newbot`
4. اتبع التعليمات
5. **احفظ التوكن**

### 2. الحصول على Chat ID

**الطريقة الأولى:**
1. ابحث عن **@userinfobot**
2. ابدأ المحادثة
3. سيعطيك معرفك

**الطريقة الثانية:**
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

### 3. اختبار البوت

```bash
# إرسال رسالة تجريبية
curl -X POST \
  https://api.telegram.org/bot<TOKEN>/sendMessage \
  -d "chat_id=<CHAT_ID>" \
  -d "text=Test message from Doser"
```

---

## 🔄 إعداد البروكسي

### تنسيق البروكسي

```
# HTTP Proxy
http://user:password@192.168.1.1:8080
http://192.168.1.1:8080

# HTTPS Proxy
https://user:password@proxy.example.com:3128

# SOCKS4
socks4://192.168.1.2:1080

# SOCKS5
socks5://user:password@192.168.1.3:1080
socks5://192.168.1.3:1080
```

### اختبار البروكسي

```bash
# HTTP Proxy
curl -x http://user:pass@ip:port https://httpbin.org/ip

# SOCKS5 Proxy
curl -x socks5://user:pass@ip:port https://httpbin.org/ip
```

### مصادر البروكسي المجانية

- [proxy-list.download](https://www.proxy-list.download/)
- [free-proxy-list.net](https://free-proxy-list.net/)
- [geonode.com](https://geonode.com/free-proxy-list)

---

## 📧 كيفية استلام رمز التحقق

### 1. تلقائياً (موصى به)

1. **أرسل رسالة** للبوت أولاً (`/start`)
2. **شغل الأداة** وانتظر
3. **سيصلك الرمز** تلقائياً في البوت
4. **تدخل الأداة** الرمز بنفسها

### 2. يدوياً

1. **شغل الأداة** بدون بوت
2. **انتظر** وصول الإيميل
3. **أرسل الرمز** يدوياً في البوت
4. **تدخل الأداة** الرمز

### 3. عبر البريد المؤقت

الأداة تدعم خدمات البريد المؤقت:
- Guerrilla Mail
- Temp Mail

---

## 🛡️ نصائح لتجنب الحظر

### 1. استخدم بروكسي

- دور بين عدة بروكسيات
- استخدم بروكسي Residentil إن أمكن
- تجنب البروكسيات المجانية العامة

### 2. تأخير مناسب

```
الحد الأدنى: 30 ثانية بين كل حساب
الموصى به: 60-120 ثانية
```

### 3. تنويع البيانات

- استخدم أسماء حقيقية
- تواريخ ميلاد مختلفة
- إيميلات مختلفة

### 4. الحدود

```
الحد الأقصى الموصى به: 5-10 حسابات/يوم
للبروكسي الواحد: 2-3 حسابات
```

---

## 📁 ملفات الإخراج

### accounts/accounts.json

```json
[
  {
    "id": 1,
    "username": "john_doe_123",
    "password": "P@ssword81297",
    "email": "john@example.com",
    "full_name": "John Doe",
    "status": "active",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### accounts.txt

```
==================================================
Username: john_doe_123
Password: P@ssword81297
Email: john@example.com
Full Name: John Doe
Status: active
Created: 2024-01-15 10:30:00
--------------------------------------------------
```

### accounts.csv

```csv
id,username,password,email,full_name,status,created_at
1,john_doe_123,P@ssword81297,john@example.com,John Doe,active,2024-01-15T10:30:00
```

---

## 🔧 خيارات متقدمة

### تغيير كلمة السر الافتراضية

1. افتح `config/settings.py`
2. عدل `DEFAULT_PASSWORD`

### تغيير نطاق العمر

في الواجهة:
- افتح تبويب Settings
- عدل Min Age و Max Age

في الكود:
```python
birthdate = generator.generate_birthdate(min_age=21, max_age=35)
```

### تخصيص User-Agent

في `config/settings.py`:
```python
USER_AGENTS = [
    "Your custom user agent",
]
```

---

## 🐛 استكشاف الأخطاء

### مشكلة: "No verification code received"

**الحل:**
1. تأكد من صحة Bot Token
2. تأكد من إرسال رسالة للبوت
3. تأكد من صحة Chat ID
4. انتظر 5 دقائق (قد يتأخر الإيميل)

### مشكلة: "Browser not opening"

**الحل:**
1. تأكد من تثبيت Chrome
2. حدث ChromeDriver:
   ```bash
   pip install --upgrade webdriver-manager
   ```
3. جرب وضع Headless

### مشكلة: "Account creation failed"

**الحل:**
1. تأكد من عدم حظر IP
2. استخدم بروكسي
3. زد التأخير
4. جرب لاحقاً

### مشكلة: "CAPTCHA detected"

**الحل:**
1. حل CAPTCHA يدوياً
2. أو انتظر انتهاء المهلة
3. أو استخدم خدمة 2captcha

---

## 📞 الدعم

للمساعدة:
- Telegram: @your_support
- GitHub: [github.com/yourusername/doser](https://github.com/yourusername/doser)

---

**🎉 استمتع باستخدام Doser!**
