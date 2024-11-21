# QuizBit Backend

QuizBit is a platform for practicing MCQ-type questions. This backend implementation provides RESTful APIs for managing questions, submitting answers, and tracking practice history.

## 🚀 Features

- User authentication using JWT
- RESTful API endpoints for:
  - Retrieving questions (list and detail)
  - Submitting answers
  - Viewing practice history
- Filtering questions by difficulty
- Automatic scoring of submitted answers
- Detailed practice history tracking

## 🛠️ Tech Stack

- Python 3.8+
- Django 4.2
- Django REST Framework
- SQLite3
- JWT Authentication

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siamkarim/QuizBit.git
   cd QuizBit
   ```

2. **Create and activate virtual environment**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure 

## 🔌 API Endpoints

### Authentication

- **POST** `/api/token/`
  - Get JWT token pair
  - Body: `{"username": "string", "password": "string"}`

- **POST** `/api/token/refresh/`
  - Refresh access token
  - Body: `{"refresh": "string"}`

### Questions

- **GET** `/api/questions/`
  - List all questions
  - Query Parameters:
    - `difficulty`: Filter by difficulty (easy, medium, hard)

- **GET** `/api/questions/{id}/`
  - Get question details
  - Parameters:
    - `id`: Question ID

- **POST** `/api/questions/{id}/submit_answer/`
  - Submit answer for a question
  - Parameters:
    - `id`: Question ID
  - Body: `{"selected_option": integer}`

## 🔒 Authentication

All API endpoints (except token generation) require JWT authentication. Include the token in the Authorization header:

Authorization: Bearer <your_access_token>

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support, email siamhossain518@gmail.com