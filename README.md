Project Setup

Prerequisites
Ensure you have the following installed:

 - Docker
 - Docker Compose
 - Python 3.10+
 - PostgreSQL
 - Redis

1. Clone the repository

git clone https://github.com/Amin7473/inventory_mgt_system.git
cd social_network_app

2. Setup .env File
Create a .env file in the project root with the following environment variables:

DB_NAME=frms_local
DB_USERNAME=amin
DB_PASSWORD=aminudeen
DB_HOST=db
DB_PORT=5432

SECRET_KEY = ''


3. Build and Run the Docker Containers
Use Docker Compose to build and start the services.

-> docker-compose up --build

This will set up:

A Django application running on port 8000
PostgreSQL database running on port 5432
Redis server running on port 6379

4. Running Migrations
Once the containers are up and running, apply the database migrations.

-> docker-compose exec web python manage.py makemigrations accounts
-> docker-compose exec web python manage.py migrate

5. Creating a Superuser
Create a superuser to access the Django admin panel.

-> docker-compose exec web python manage.py createsuperuser

Follow the prompts to set up the superuser account.

6. Access the Application
Open the application in your browser at http://localhost:8000
Access the Django Admin at http://localhost:8000/admin

7. Load Postman Collection
Import the file postman_api_collection.json available in the
project root directory in Postman and access the APIs and their sample responses

8. Redis Integration
Redis has been added for caching and rate-limiting tasks. The Redis instance runs on redis://redis:6379.

9. API Documentation
PDF document for apis in project root directory : API_Documentation.pdf

10. Test Cases
To run the test cases , simply run command:
docker-compose exec web python manage.py test