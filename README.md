# Yangiliklar API — Django + PostgreSQL

## Loyha haqida

Django REST Framework va PostgreSQL asosida qurilgan yangiliklar veb-sayti uchun backend API.

## Rollar

| Rol | Ro'yxatdan o'tishda tanlanadi | Imkoniyatlar |
| `user` | ✅ Ha | Yangiliklar o'qish, izoh yozish |
| `journalist` | ✅ Ha | Yangilik CRUD, izohlarni ko'rish |
| `admin` | ❌ Yo'q (faqat Django admin panelidan) | Hamma narsani boshqarish |

> **Muhim:** Ro'yxatdan o'tishda faqat `user` va `journalist` tanlash mumkin.  
> Admin roli faqat `python manage.py createsuperuser` yoki Django admin paneli orqali beriladi.

## O'rnatish

### 1. Loyihani yuklab oling

git clone <repo_url>
cd news_api

### 2. Virtual muhit yarating

python -m venv venv
source venv/bin/activate        
venv\Scripts\activate          

### 3. Kutubxonalarni o'rnating

pip install -r requirements.txt

### 4. `.env` faylini yarating


cp .env.example .env

### 5. PostgreSQL bazasini yarating

CREATE DATABASE news_db;

### 6. Migratsiyalarni bajaring

python manage.py makemigrations
python manage.py migrate

### 7. Superuser (admin) yarating

python manage.py createsuperuser

### 8. Serverni ishga tushiring

python manage.py runserver

## API Endpointlar

### 🔐 Autentifikatsiya (`/api/auth/`)

| Method | URL | Tavsif | Ruxsat |
|--------|-----|--------|--------|
| POST | `/api/auth/register/` | Ro'yxatdan o'tish (`user` yoki `journalist`) | Hammaga |
| POST | `/api/auth/login/` | Kirish (JWT token olish) | Hammaga |
| POST | `/api/auth/logout/` | Chiqish (tokenni bekor qilish) | Login qilgan |
| POST | `/api/auth/token/refresh/` | Access tokenni yangilash | Login qilgan |
| GET | `/api/auth/profile/` | O'z profilini ko'rish | Login qilgan |
| PATCH | `/api/auth/profile/` | Profilni tahrirlash | Login qilgan |
| POST | `/api/auth/profile/change-password/` | Parolni o'zgartirish | Login qilgan |

#### Ro'yxatdan o'tish namunasi
```json
POST /api/auth/register/
{
  "username": "ali_user",
  "email": "ali@example.com",
  "password": "Str0ngPass!",
  "password2": "Str0ngPass!",
  "role": "user",
  "first_name": "Ali",
  "last_name": "Valiyev"
}
```

#### Kirish namunasi
```json
POST /api/auth/login/
{
  "username": "ali_user",
  "password": "Str0ngPass!"
}
```

---

### 📰 Yangiliklar (`/api/news/`)

| Method | URL | Tavsif | Ruxsat |
|--------|-----|--------|--------|
| GET | `/api/news/` | Chop etilgan yangiliklar ro'yxati | user, journalist, admin |
| GET | `/api/news/<id>/` | Yangilik tafsiloti | user, journalist, admin |
| POST | `/api/news/create/` | Yangilik yaratish | Faqat journalist |
| PATCH | `/api/news/<id>/update/` | Yangilikni tahrirlash | journalist (o'ziniki), admin (barchasi) |
| DELETE | `/api/news/<id>/delete/` | Yangilikni o'chirish | journalist (o'ziniki), admin (barchasi) |
| GET | `/api/news/my/` | O'z yangiliklarim (draft+published) | Faqat journalist |

#### Filtrlash
```
GET /api/news/?category=texnologiya
GET /api/news/?search=sun'iy intellekt
```

#### Yangilik yaratish namunasi
```json
POST /api/news/create/
Authorization: Bearer <journalist_token>

{
  "title": "O'zbekistonda sun'iy intellekt rivojlanmoqda",
  "content": "Yangilik matni bu yerda...",
  "category": 1,
  "status": "published"
}
```

---

### 💬 Izohlar (`/api/comments/`)

| Method | URL | Tavsif | Ruxsat |
|--------|-----|--------|--------|
| GET | `/api/news/<news_id>/comments/` | Yangilik izohlari | user, journalist, admin |
| POST | `/api/comments/create/` | Izoh qo'shish | Faqat **user** (bloklangan emas) |
| DELETE | `/api/comments/<id>/delete/` | Izoh o'chirish | user (o'ziniki), admin (barchasi) |
| GET | `/api/comments/my-news/` | O'z yangiliklaridagi izohlar | Faqat journalist |
| GET | `/api/admin/comments/` | Barcha izohlar | Faqat admin |

#### Izoh yozish namunasi
```json
POST /api/comments/create/
Authorization: Bearer <user_token>

{
  "news": 5,
  "text": "Juda qiziqarli yangilik!"
}
```

---

### 🛡️ Admin (`/api/auth/admin/`)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/auth/admin/users/` | Barcha foydalanuvchi/jurnalistlar |
| GET | `/api/auth/admin/users/?role=user` | Faqat foydalanuvchilar |
| GET | `/api/auth/admin/users/?role=journalist` | Faqat jurnalistlar |
| POST | `/api/auth/admin/users/<id>/block/` | Bloklash |
| DELETE | `/api/auth/admin/users/<id>/block/` | Blokdan chiqarish |
| DELETE | `/api/auth/admin/news/<id>/delete/` | Yangilikni o'chirish |
| GET | `/api/admin/comments/` | Barcha izohlar |
| DELETE | `/api/comments/<id>/delete/` | Izohni o'chirish |

#### Bloklash namunasi (muddatli)
```json
POST /api/auth/admin/users/3/block/
Authorization: Bearer <admin_token>

{
  "blocked_until": "2026-05-01T00:00:00Z",
  "block_reason": "Spam izohlar yozgan"
}
```

#### Doimiy bloklash
```json
POST /api/auth/admin/users/3/block/
Authorization: Bearer <admin_token>

{
  "block_reason": "Qoidalar buzilishi"
}
```

---

### 📚 Kategoriyalar

| Method | URL | Tavsif | Ruxsat |
|--------|-----|--------|--------|
| GET | `/api/categories/` | Barcha kategoriyalar | Hammaga |

---

## 📖 Swagger hujjatlar

Server ishga tushgandan keyin:
- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/
- **Django Admin:** http://localhost:8000/admin/

---

## Loyha strukturasi

```
news_api/
├── manage.py
├── requirements.txt
├── .env.example
├── news_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── accounts/          
    │   ├── models.py      
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── permissions.py 
    │   └── admin.py
    ├── news/              
    │   ├── models.py      
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── admin.py
    └── comments/          
        ├── models.py
        ├── serializers.py
        ├── views.py
        ├── urls.py
        └── admin.py
```

---

## Bloklash mexanizmi

- **Muddatli bloklash:** `blocked_until` vaqti o'tgach, foydalanuvchi **avtomatik** blokdan chiqadi (keyingi kirish yoki so'rovda tekshiriladi).
- **Doimiy bloklash:** `blocked_until` bo'sh qoldirilsa — faqat admin qo'lda blokdan chiqaradi.
- Bloklangan foydalanuvchi login qilganda xato xabari va muddati ko'rsatiladi.

---

## Xavfsizlik

- JWT token asosidagi autentifikatsiya (access: 2 soat, refresh: 7 kun)
- Har bir so'rovda `IsNotBlocked` tekshiruvi
- Admin roli API orqali **hech qachon** berilmaydi
- Parol Django standart validatorlari orqali tekshiriladi
