# JULO Mini Wallet Exercise

I have developed a mini wallet REST API exercise project using the Python programming language and the Django framework. The project aims to fulfill the specified requirements for request and response expectations. The Django version used in this project is 5.0.1, and additional libraries have been incorporated to enhance functionality.

The project focuses on creating a RESTful API for a mini wallet system, allowing users to perform various wallet-related operations. It provides endpoints for actions such as wallet registration, balance inquiry, fund deposit, fund withdrawal, and transaction history retrieval.

By utilizing the Django framework, the project benefits from its robust features, including built-in authentication, database management, and URL routing. The Django REST framework is also utilized to simplify API development, providing tools for serialization, viewsets, and authentication mechanisms.

The project adheres to the principles of RESTful design and follows best practices for API development. It aims to provide a secure, efficient, and user-friendly experience for interacting with the mini wallet system.

Overall, the mini wallet REST API exercise project serves as a practical demonstration of Python and Django's capabilities in building robust and scalable web applications.

```txt
julo-mini-wallet/
├── apiv1/
│   ├── wallet/
│   │   ├── entities.py
│   │   ├── handlers.py
│   │   ├── repositories.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   └── validators.py
│   ├── __init__.py
│   └── urls.py
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── models/
│   ├── auth_data/
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── wallet/
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── vars.py
│   ├── wallet_transaction/
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── vars.py
│   └── __init__.py
├── utils/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   └── helpers/
│       ├── auth.py
│       └── string.py
├── manage.py
└── requirements.txt

```

## How to Use
### Requirements
- Python version: 3.10 or higher

### Installation
- Clone the project repository from the source.
- Create a virtual environment for the project:
  ```sh
  python3 -m venv myenv
  ```
- Activate the virtual environment:
    - For Windows:
      ```sh
      myenv\Scripts\activate
      ```
    - For macOS/Linux:
      ```sh
      source myenv/bin/activate
      ```
- Install the project dependencies:
  ```
  pip install -r requirements.txt
  ```

### Database Migration
- Make sure you have a configured database in the project's settings.
- Apply the initial database migration:
  ```sh
  python manage.py migrate
  ```

### Running the Server
- Start the development server:
  ```sh
  python manage.py runserver
  ```
- Open your web browser and visit http://localhost:8000 to access the application.

### Additional Configuration
To customize the project settings, refer to the `core/settings.py` file in the project directory.

## Run using Docker
- Using published docker image
  ```sh
  docker run -d ruriazz/julo-mini-wallet-exercise:latest
  ```
- Using docker-compose file with compatible published docker image or build image locally
  ```sh
  docker-compose up -d
  ```
- Using docker-compose file with build image locally
  ```sh
  docker compose up -d --build
  ```

## Trying out this online application
- Url https://miniwallet.ruriazz.com
- Testing Database:
  ```txt
  == MySQL ==
  Name: julo_mini_wallet_exercise
  Host: 8.215.37.245
  Port: 3306
  User: testinguser
  Pass: testingpassword
  ```