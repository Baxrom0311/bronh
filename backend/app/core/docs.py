OPENAPI_DESCRIPTION = """
Respiratory CDSS backend API.

Bu hujjat Swagger UI orqali tizimni tez tekshirish uchun tayyorlangan.

Asosiy oqim:
1. `POST /auth/register` yoki `POST /auth/login`
2. Swagger ichida `Authorize` orqali `Bearer <access_token>` yuborish
3. `POST /patients/`
4. `POST /symptoms/`
5. `POST /diagnoses/`

Role-based endpointlar:
- `doctor/admin`: diagnosis confirmation
- `admin`: stats, users, ML metadata, retrain
"""

OPENAPI_TAGS = [
    {"name": "health", "description": "Service holati va model metadata endpointlari."},
    {"name": "auth", "description": "Register, login, refresh, logout va joriy user endpointlari."},
    {"name": "patients", "description": "Patient profili yaratish va ko'rish endpointlari."},
    {"name": "symptoms", "description": "Symptom record yaratish va o'qish endpointlari."},
    {"name": "diagnoses", "description": "CDSS diagnosis yaratish, tarix va doctor confirmation endpointlari."},
    {"name": "admin", "description": "Platforma statistikasi va foydalanuvchilar ro'yxati."},
    {"name": "admin-ml", "description": "ML metadata va retrain boshqaruvi."},
]

SWAGGER_UI_PARAMETERS = {
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "docExpansion": "list",
    "filter": True,
    "tryItOutEnabled": True,
}
