🌐 Social Media API — Follow System & Feed Feature
📘 Overview

This project is a Django REST Framework (DRF)-powered Social Media API that enables users to connect through posts, comments, and follow relationships.

Users can:

🔐 Register and log in with token-based authentication

👥 Follow and unfollow other users

🧵 View a personalized feed showing posts from followed users

✍️ Create, edit, and delete their own posts and comments

🚀 Live Demo

Base URL: https://ibrahim-sma.onrender.com

Example endpoints:

/api/accounts/register/ → Register a new user

/api/accounts/login/ → Log in and receive a token

/api/accounts/follow/<user_id>/ → Follow a user

/api/feed/ → Get feed from followed users

🧰 Tech Stack

Backend: Django, Django REST Framework

Database: PostgreSQL

Authentication: Token Authentication (DRF)

Hosting: Render


⚙️ Local Setup

Clone the repo:

https://github.com/Kwanza247/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api



Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # for macOS/Linux
venv\Scripts\activate      # for Windows

pip install -r requirements.txt


Run migrations:

python manage.py makemigrations
python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Visit:

http://127.0.0.1:8000/

🔗 API Endpoints
Authentication
Method	Endpoint	Description
POST	/api/accounts/register/	Register new user
POST	/api/accounts/login/	Log in and receive token
GET	/api/accounts/profile/	Get current user profile
POST	/api/accounts/follow/<user_id>/	Follow a user
POST	/api/accounts/unfollow/<user_id>/	Unfollow a user
Posts
Method	Endpoint	Description
GET	/api/posts/	List all posts
POST	/api/posts/	Create new post
GET	/api/posts/<id>/	Retrieve single post
PUT	/api/posts/<id>/	Update post
DELETE	/api/posts/<id>/	Delete post
Feed
Method	Endpoint	Description
GET	/api/feed/	Posts from followed users
🔐 Authentication Example

Register

POST /api/accounts/register/
{
  "username": "ibrahim",
  "email": "ibrahim@example.com",
  "password": "mypassword"
}


Login

POST /api/accounts/login/
{
  "username": "ibrahim",
  "password": "mypassword"
}


Response:

{
  "token": "your-auth-token"
}


Use the token in headers for authenticated requests:

Authorization: Token your-auth-token

📁 Project Structure
social_media_api/
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── posts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── manage.py
└── README.md

✅ Features Summary

Custom user model with following relationships

Token-based authentication

CRUD operations for posts and comments

Personalized feed endpoint

Pagination, filtering, and search support