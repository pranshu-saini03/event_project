# Event Management System

A Django-based event management platform that allows users to book venues and manage event bookings with JWT authentication.

## Features

- **User Authentication**: Register and login with role-based access control (Admin, Owner, User)
- **Venue Management**: Create, update, and delete venues (Owner only)
- **Availability Management**: Add availability dates for venues
- **Booking System**: Book venues for specific dates
- **JWT Authentication**: Secure API endpoints with JWT tokens
- **Pagination**: List venues with pagination support

## Tech Stack

- **Framework**: Django 6.0.1
- **Database**: PostgreSQL
- **Authentication**: JWT (PyJWT)
- **Language**: Python 3.x

## Project Structure

```
eventproject/
├── accounts/           # User authentication and permissions
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── venue/             # Venue management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── decorator.py
│   └── manager.py
├── booking/           # Booking management
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── eventproject/      # Project settings and configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── middleware/    # JWT authentication middleware
│   └── utils/         # JWT utilities
├── manage.py
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eventproject
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

6. **Configure Database**
   Update `eventproject/settings.py` with your PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'event_management',
           'USER': 'your_postgres_user',
           'PASSWORD': 'your_postgres_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

7. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /auth/register/` - Register a new user
- `POST /auth/login/` - Login and get JWT token
- `POST /auth/logout/` - Logout user

### Venues (Owner/Admin)

- `POST /api/venues/` - Create a new venue
- `PUT /api/venues/` - Update venue details
- `DELETE /api/venues/` - Delete a venue
- `GET /api/venues/` - List venues (with pagination and filters)

### Availability

- `POST /api/venues/availability/` - Add availability date for a venue

### Bookings

- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/` - List user bookings
- `GET /api/bookings/<id>/` - Get booking details
- `PUT /api/bookings/<id>/` - Update booking status

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key for security | `your-secret-key` |
| `DEBUG` | Debug mode (True/False) | `True` |

## User Roles

1. **Admin**: Full access to all features
2. **Owner**: Can create and manage their own venues
3. **User**: Can browse venues and make bookings

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Database Models

- **User**: User accounts with roles
- **OwnerPermission**: Permission management for owners
- **Venue**: Venue details and metadata
- **VenueAvailability**: Available dates for venues
- **Booking**: Venue bookings by users

## Development

### Running Tests
```bash
python manage.py test
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush
```

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@eventmanagement.com or create an issue in the repository.
