# 🤝 Contributing to Doser

شكراً لاهتمامك بالمساهمة في Doser!

---

## 🚀 كيفية المساهمة

### 1. الإبلاغ عن الأخطاء (Bug Reports)

عند الإبلاغ عن خطأ، يرجى تضمين:
- وصف واضح للمشكلة
- خطوات إعادة إنتاج الخطأ
- رسالة الخطأ الكاملة
- إصدار Python والنظام
- لقطات شاشة (إن أمكن)

### 2. اقتراح ميزات جديدة (Feature Requests)

- وصف الميزة بوضوح
- شرح الفائدة المتوقعة
- أمثلة على الاستخدام

### 3. Pull Requests

1. **Fork** المستودع
2. **Clone** fork الخاص بك
3. **Create branch** جديدة
4. **Commit** التغييرات
5. **Push** إلى fork
6. **Open Pull Request**

---

## 📋 معايير الكود

### Python Style Guide

اتبع [PEP 8](https://pep8.org/):

```python
# ✅ Good
def create_account(username: str, password: str) -> dict:
    """Create a new Instagram account.
    
    Args:
        username: The desired username
        password: The account password
        
    Returns:
        dict containing account info
    """
    return {'username': username, 'password': password}

# ❌ Bad
def create_account(username, password):
    return {'username':username,'password':password}
```

### التعليقات

- استخدم docstrings لجميع الدوال
- اكتب تعليقات بالإنجليزية
- اشرح "لماذا" وليس "ماذا"

### التسميات

- `snake_case` للدوال والمتغيرات
- `PascalCase` للClasses
- `UPPER_CASE` للثوابت

---

## 🧪 الاختبارات

### تشغيل الاختبارات

```bash
python test_bot.py
```

### إضافة اختبارات جديدة

```python
def test_new_feature():
    """Test description"""
    # Arrange
    input_data = "test"
    
    # Act
    result = new_feature(input_data)
    
    # Assert
    assert result == expected_output
```

---

## 📁 هيكل المشروع

```
doser/
├── config/          # الإعدادات
├── core/            # المنطق الرئيسي
├── gui/             # الواجهة الرسومية
├── utils/           # الأدوات المساعدة
├── tests/           # الاختبارات
└── docs/            # التوثيق
```

---

## 🎯 أولويات التطوير

### قيد التنفيذ
- [ ] دعم CAPTCHA التلقائي
- [ ] تحسين التعامل مع الأخطاء
- [ ] دعم متعدد اللغات

### مخطط للمستقبل
- [ ] دعم منصات أخرى (Twitter, TikTok)
- [ ] واجهة ويب
- [ ] API REST

### مقبول
- [x] واجهة رسومية
- [x] دعم البروكسي
- [x] إدارة الحسابات

---

## 💬 التواصل

- Telegram: @your_support
- GitHub Discussions
- Email: support@doser.app

---

## 🏆 المساهمون

شكراً لجميع المساهمين!

---

**✨ معاً نبني أداة أفضل!**
