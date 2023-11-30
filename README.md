## Description
A simple real-time To Do List with Websockets and accounts.


## Installation
1. Create a virtual environment and activate it:
```
python -m venv venv && venv\scripts\activate
```
2. Install required dependencies:
```
python -m pip install -r requirements.txt
```
3. Make migrations and migrate:
```
python manage.py makemigrations && python manage.py migrate
```
4. Create a `.env` file with environment variables:
```
DJANGO_SECRET_KEY="your_django_key"
ALLOWED_HOSTS=127.0.0.1 localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1

# These are default recaptcha test keys
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe

TDL_WS_CONTAINER_NAME=tdl_ws
DEBUG=1
```
5. Run local server:
```
python manage.py runserver
```