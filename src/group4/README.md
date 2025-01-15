# پروژه گروه 4

این پروژه شامل یک برنامه جنگو است که شامل فایل‌ها و پوشه‌های مختلف برای پیاده‌سازی بخش‌های مختلف است.

## ساختار پروژه
group4/
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
├── views.py
├── __init__.py
├── datasets/
│   └── fa.csv
├── logic/
│   ├── miss_spell_finder.py
│   └── confs/
│       └── consts.py
├── migrations/
│   ├── 0001_initial.py
│   └── __init__.py
├── static/
│   ├── script.js
│   ├── style.css
│   ├── view/
│       ├── pencil_white.ico
│       ├── css/
│       │   ├── bootstrap.min.css
│       │   ├── font-awesome.min.css
│       │   └── style.css
│       ├── fonts/
│           ├── fontawesome-webfont.eot
│           ├── fontawesome-webfont.svg
│           ├── fontawesome-webfont.ttf
│           ├── fontawesome-webfont.woff
│           ├── fontawesome-webfont.woff2
│           ├── FontAwesome.otf
│           ├── Vazir.eot
│           ├── Vazir.ttf
│           ├── Vazir.woff
│           └── Vazir.woff2
├── templates/
│   └── index.html
└── __pycache__/## پیش‌نیازها
- Python 3.11 یا بالاتر
- Django 4.0 یا بالاتر

## نصب و اجرا
1. ابتدا پیش‌نیازها را نصب کنید:
  
     pip install -r requirements.txt
        2. مهاجرت پایگاه داده را اجرا کنید:
          
             python manage.py makemigrations
                python manage.py migrate
                   3. سرور توسعه را اجرا کنید:
                     
                        python manage.py runserver
                           4. برنامه در مرورگر در آدرس http://127.0.0.1:8000 قابل دسترسی است.

## توضیحات بیشتر
- datasets/fa.csv: شامل داده‌های مورد استفاده در برنامه.
- logic/miss_spell_finder.py: ماژول تشخیص خطاهای املایی.
- static/: فایل‌های استاتیک شامل CSS، JS و فونت‌ها.
- templates/index.html: قالب اصلی برنامه.

