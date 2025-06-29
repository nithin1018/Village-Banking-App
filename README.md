# Village Banking System

A comprehensive Django REST API banking system designed for village communities, featuring user management, account operations, transaction processing, and administrative controls with secure authentication and real-time transaction monitoring.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [User Roles](#user-roles)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Transaction System](#transaction-system)
- [Admin Dashboard](#admin-dashboard)
- [Security Features](#security-features)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Banking Features
- **User Registration & Authentication** - Secure email-based user registration with profile type selection
- **Multi-role System** - Support for Users, Staff, and Admin roles with employee ID validation
- **Automatic Account Creation** - Auto-generated unique 6-digit account numbers for users via Django signals
- **Complete Transaction System** - Deposit, withdrawal, and transfer operations with atomic database transactions
- **Real-time Balance Updates** - Instant balance updates with transaction validation and rollback on failure
- **Comprehensive Transaction History** - Complete audit trail with filtering by type, status, and date
- **Secure OTP System** - Email-based OTP verification for password reset with 5-minute expiry
- **Profile Management** - User profile updates with Cloudinary image upload support
- **Phone Number Validation** - International phone number validation with regional support (India)

### Advanced Security Features
- **JWT Authentication** - Secure token-based authentication with custom claims including user role
- **Token Blacklisting** - Secure logout with refresh token blacklisting
- **Custom Password Validation** - Minimum 6 characters with uppercase and alphabet requirements
- **Rate Limiting** - Custom throttling for OTP requests, transactions, and general API usage
- **CORS Configuration** - Cross-origin resource sharing with custom headers
- **Input Validation & Sanitization** - Comprehensive data validation with custom validators
- **Atomic Transactions** - Database-level transaction atomicity ensuring data consistency
- **Permission-based Access Control** - Role-based permissions with custom permission classes

### Administrative Features
- **Comprehensive Admin Dashboard** - Real-time statistics including total users and bank balance
- **User Management System** - View, search, and filter all users with detailed profiles
- **Transaction Monitoring** - Monitor all system transactions with advanced filtering
- **Staff Management** - Manage staff accounts with employee ID requirements
- **Advanced Search & Filtering** - Filter users by name, email, phone, account number
- **Transaction Analytics** - Filter transactions by type (deposit/withdraw/transfer) and status
- **Detailed User Profiles** - Complete user information including account and transaction history

## Technology Stack

### Backend Framework
- **Django 5.2.3** - Modern Python web framework with latest features
- **Django REST Framework 3.16.0** - Powerful REST API development toolkit
- **PostgreSQL** - Robust relational database with psycopg2 adapter
- **JWT Authentication** - djangorestframework-simplejwt 5.5.0 for secure token-based auth

### Third-Party Integrations
- **Cloudinary** - Cloud-based image storage and management for profile pictures
- **Gmail SMTP** - Email service for OTP delivery with threading support
- **Phone Number Validation** - django-phonenumber-field with international support

### Development & Deployment Tools
- **django-filter 25.1** - Advanced filtering capabilities for APIs
- **django-cors-headers 4.7.0** - CORS handling for cross-origin requests
- **django-ratelimit 4.1.0** - Custom rate limiting and throttling
- **drf-spectacular 0.28.0** - Automated OpenAPI schema generation and documentation
- **Gunicorn 23.0.0** - Production-ready WSGI HTTP Server
- **WhiteNoise 6.9.0** - Static file serving for production

## Project Structure

```
village_banking/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── Procfile                     # Heroku deployment configuration
├── README.md                    # Project documentation
├── village_banking/             # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings with environment variables
│   ├── urls.py                  # Main URL routing with API documentation
│   ├── wsgi.py                  # WSGI configuration for deployment
│   └── asgi.py                  # ASGI configuration for async support
└── user_accounts/               # Main application module
    ├── models.py                # Database models (Profile, Account, Transaction)
    ├── serializers.py           # DRF serializers for API data validation
    ├── views.py                 # API views with permission and throttling
    ├── urls.py                  # Application URL routing
    ├── admin.py                 # Django admin interface configuration
    ├── filters.py               # Custom filtering for transactions and profiles
    ├── validators.py            # Custom field validators
    ├── services.py              # Business logic for transaction processing
    ├── signals.py               # Django signals for automatic account creation
    ├── permission.py            # Custom permission classes
    ├── throttles.py             # Custom rate limiting classes
    ├── utils.py                 # Utility functions (OTP, email, account generation)
    ├── tests.py                 # Unit tests
    └── migrations/              # Database migration files
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd village_banking
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   # On Windows
   myenv\Scripts\activate
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/village_banking
   
   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Configuration

### Database Configuration
The system supports PostgreSQL as the primary database. Configure your database URL in the environment variables.

### Email Configuration
Configure SMTP settings for OTP delivery:
- Gmail SMTP is pre-configured
- Use app-specific passwords for Gmail
- Update EMAIL_* variables in .env file

### Cloudinary Setup
For image storage:
1. Create a Cloudinary account
2. Get your cloud name, API key, and API secret
3. Add them to your .env file

## API Endpoints

### Authentication Endpoints
```
POST /api/profile/register/                    # User registration with role selection
POST /api/profile/login/                       # User login with JWT token generation
POST /api/profile/login/refresh/               # JWT token refresh
PATCH /api/profile/logout/                     # Secure logout with token blacklisting
PATCH /api/profile/change-password/            # Change password for authenticated users
POST /api/profile/login/sentotp/               # Send OTP to email for password reset
POST /api/profile/login/forgot-password/       # Reset password using OTP verification
```

### User Profile Endpoints
```
GET  /api/profile/                             # Get current user profile with account details
GET  /api/profile/<id>/                        # Get specific user profile and account info
```

### Transaction Endpoints
```
POST /api/profile/transaction/                 # Create transaction (deposit/withdraw/transfer)
```

### Admin Dashboard Endpoints
```
GET  /api/admin/dashboard/                     # Admin dashboard with system statistics
GET  /api/admin/dashboard/profile/             # List all users with filtering and search
GET  /api/admin/dashboard/profile/<id>/        # Get detailed user profile for admin
GET  /api/admin/dashboard/transaction/         # List all transactions with filtering
GET  /api/admin/dashboard/transaction/<id>/    # Get detailed transaction information
```

### API Documentation Endpoints
```
GET  /schema/                                  # OpenAPI schema
GET  /schema/swagger/                          # Swagger UI documentation
GET  /schema/redoc/                           # ReDoc documentation
GET  /ping/                                   # Health check endpoint
```

## User Roles & Permissions

### User (Default Role)
- **Account Management**: Automatically created account with unique 6-digit account number
- **Transaction Operations**: Perform deposits, withdrawals, and transfers
- **Balance Inquiry**: Real-time balance checking and transaction history
- **Profile Management**: Update personal information and profile picture
- **Security**: Change password and request OTP for password reset
- **Access Control**: Can only access own account and transaction data

### Staff Role
- **User Permissions**: All standard user permissions and capabilities
- **Employee Identification**: Requires valid employee_id during registration
- **Enhanced Access**: Limited administrative access to user data
- **Staff Status**: Automatically granted Django staff status (is_staff=True)
- **Registration Validation**: Employee ID validation for staff account creation

### Admin Role
- **Full System Access**: Complete administrative control over the banking system
- **User Management**: View, search, and manage all user accounts
- **Transaction Oversight**: Monitor and analyze all system transactions
- **Dashboard Analytics**: Access to system statistics and performance metrics
- **Staff Management**: Create and manage staff accounts with employee IDs
- **Superuser Privileges**: Full Django admin access (is_staff=True, is_superuser=True)
- **Advanced Filtering**: Filter users and transactions by multiple criteria

## Database Models

### Profile Model (Custom User Model)
```python
# Extends Django's AbstractUser with custom fields
- first_name: CharField (validated for alphabets only)
- last_name: CharField (validated for alphabets only)  
- age: IntegerField (minimum 18 years validation)
- email: EmailField (unique, used as USERNAME_FIELD)
- phonenumber: PhoneNumberField (unique, region='IN')
- profile_type: CharField (choices: user/staff/admin)
- employee_id: CharField (required for staff/admin)
- profile_pic: CloudinaryField (optional image upload)
- otp: CharField (hashed OTP for password reset)
- otp_created_time: DateTimeField (OTP expiry tracking)
- created_at/updated_at: Automatic timestamps
```

### Account Model
```python
# One-to-one relationship with Profile
- user: OneToOneField (linked to Profile)
- account_number: CharField (auto-generated 6-digit unique number)
- balance: DecimalField (default=0.00, max_digits=12, decimal_places=2)
- created_at/updated_at: Automatic timestamps
# Note: Automatically created for users via Django signals
```

### Transaction Model
```python
# Complete transaction logging system
- transaction_type: CharField (choices: withdraw/deposit/transfer)
- sender: ForeignKey (Account, nullable for deposits)
- receiver: ForeignKey (Account, nullable for withdrawals)
- amount: DecimalField (max_digits=12, decimal_places=2)
- status: CharField (choices: success/failed/pending)
- description: TextField (optional transaction description)
- timestamp: DateTimeField (auto_now_add=True)
```

## Authentication System

The system implements a sophisticated JWT-based authentication system with enhanced security features:

### JWT Token Implementation
- **Access Tokens**: Short-lived tokens for API access with custom claims
- **Refresh Tokens**: Long-lived tokens for obtaining new access tokens
- **Token Blacklisting**: Secure logout functionality that invalidates refresh tokens
- **Custom Claims**: Includes user email, profile_type, is_staff, and is_superuser in tokens

### Custom Token Claims
```python
{
    "email": "user@example.com",
    "profile_type": "user|staff|admin", 
    "is_staff": true|false,
    "is_superuser": true|false
}
```

### Authentication Flow
1. **Registration**: User registers with email, password, and profile type
2. **Login**: Email/password validation returns access and refresh tokens
3. **API Access**: Include access token in Authorization header
4. **Token Refresh**: Use refresh token to get new access tokens
5. **Logout**: Blacklist refresh token for secure session termination

### Security Features
- **Password Validation**: Minimum 6 characters, must contain alphabets and uppercase
- **Email Uniqueness**: Prevents duplicate email registrations
- **Phone Number Validation**: International format validation with India region default
- **OTP System**: 4-digit OTP with 5-minute expiry for password reset

### Token Usage
```python
# Include in request headers
Authorization: Bearer <access_token>
```

## Transaction System

The transaction system provides secure, atomic banking operations with comprehensive validation:

### Transaction Types & Logic

#### 1. Deposit Operations
- **Process**: Add money to user account
- **Validation**: Amount must be positive
- **Database**: Updates receiver account balance
- **Atomicity**: Single database transaction

#### 2. Withdrawal Operations  
- **Process**: Remove money from user account
- **Validation**: Sufficient balance check before processing
- **Database**: Updates sender account balance
- **Error Handling**: Failed status if insufficient funds

#### 3. Transfer Operations
- **Process**: Send money between accounts
- **Validation**: 
  - Sufficient sender balance
  - Valid receiver account number
  - Prevents self-transfers
- **Database**: Atomic update of both sender and receiver balances
- **Error Handling**: Transaction rollback on any failure

### Transaction Processing Flow
1. **Input Validation**: Validate transaction data and account numbers
2. **Account Verification**: Verify sender and receiver accounts exist
3. **Balance Verification**: Check sufficient funds for withdrawals/transfers
4. **Atomic Processing**: Execute transaction within database transaction
5. **Balance Updates**: Update account balances in real-time
6. **Transaction Logging**: Record complete transaction details
7. **Status Setting**: Set success/failed status based on operation result

### Transaction Validation Rules
- **Minimum Amount**: Must be greater than zero
- **Account Numbers**: 6-digit unique account number validation
- **Self-Transfer Prevention**: Users cannot transfer to their own account
- **Balance Sufficiency**: Withdrawals and transfers check available balance
- **Receiver Requirement**: Transfer operations require valid receiver account

### Atomic Transaction Safety
- All database operations wrapped in `@db_transaction.atomic()`
- Automatic rollback on any operation failure
- Consistent balance updates across all accounts
- Transaction status accurately reflects operation result

### Transaction Status Tracking
- **Success**: Transaction completed successfully
- **Failed**: Transaction failed due to validation or insufficient funds
- **Pending**: Transaction initiated but not yet processed (future use)

## Admin Dashboard

The admin dashboard provides comprehensive system oversight and management capabilities:

### Dashboard Analytics
- **System Statistics**: 
  - Total number of users in the system
  - Total bank balance across all accounts
  - Current admin user information
- **Real-time Data**: Live statistics updated with each request

### User Management Features
- **Complete User List**: View all users with pagination support
- **Advanced Filtering**:
  - Filter by full name (first_name + last_name)
  - Filter by email (case-insensitive partial matching)
  - Filter by phone number (partial matching)
  - Filter by account number (partial matching)
- **Sorting Options**: Sort by first_name, age, or created_at
- **Detailed User Profiles**: Access complete user information including account and transaction history

### Transaction Monitoring
- **System-wide Transaction View**: Monitor all transactions across the platform
- **Transaction Filtering**:
  - Filter by transaction type (deposit/withdraw/transfer)
  - Filter by status (success/failed/pending)
- **Sorting Capabilities**: Sort by transaction ID or timestamp
- **Detailed Transaction View**: Access complete transaction details including sender/receiver information

### Administrative Controls
- **Role-based Access**: Only admin and staff can access dashboard features
- **Secure Permissions**: Custom permission classes ensure proper access control
- **Rate Limiting**: Throttling applied to prevent admin API abuse

## Security Features

### Authentication Security
- **JWT Token Security**: Secure token generation with custom claims
- **Password Hashing**: Django's built-in password hashing with salt
- **Token Blacklisting**: Prevents replay attacks after logout
- **Session Security**: Stateless authentication reduces session hijacking risks

### API Security
- **Rate Limiting**: Custom throttling classes for different operations
  - OTP requests: Limited to prevent spam
  - Transaction operations: Controlled for security
  - General API: User and anonymous rate limits
- **CORS Configuration**: Controlled cross-origin access
- **Input Validation**: Comprehensive validation at multiple layers
- **SQL Injection Prevention**: Django ORM provides automatic protection

### Data Security
- **Field Validation**: Custom validators for names, age, and amounts
- **Phone Number Validation**: International format validation
- **Email Validation**: Django's built-in email validation
- **File Upload Security**: Cloudinary integration for secure image uploads

### Business Logic Security
- **Atomic Transactions**: Database consistency guaranteed
- **Balance Validation**: Prevents overdrafts and negative balances
- **Account Number Uniqueness**: Prevents duplicate account creation
- **Self-Transfer Prevention**: Users cannot transfer to themselves

### OTP Security
- **Secure Generation**: Random 4-digit OTP generation
- **Hashed Storage**: OTPs stored using Django's password hashing
- **Time-based Expiry**: 5-minute expiry for security
- **Single Use**: OTPs invalidated after successful use

## API Documentation

The API is fully documented using drf-spectacular with OpenAPI 3.0 specification:

### Documentation Access
- **Swagger UI**: `/schema/swagger/` - Interactive API documentation with request/response examples
- **ReDoc**: `/schema/redoc/` - Beautiful, responsive API documentation
- **OpenAPI Schema**: `/schema/` - Raw OpenAPI 3.0 JSON schema
- **Health Check**: `/ping/` - Simple health check endpoint returning `{"status": "ok"}`

### API Features
- **Interactive Testing**: Test API endpoints directly from Swagger UI
- **Request/Response Examples**: Complete examples for all endpoints
- **Authentication Documentation**: JWT token usage examples
- **Error Response Documentation**: Detailed error codes and messages
- **Filtering Documentation**: Query parameter examples for filtering

## Error Handling

The system implements comprehensive error handling with detailed error responses:

### Validation Errors
```json
{
  "field_name": [
    "Detailed error message with error code"
  ]
}
```

### Authentication Errors
```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

### Business Logic Errors
```json
{
  "error": "Insufficient Balance"
}
```

### Common Error Types
- **400 Bad Request**: Validation errors, business logic violations
- **401 Unauthorized**: Authentication required or invalid tokens
- **403 Forbidden**: Permission denied for requested resource
- **404 Not Found**: Resource not found (user, account, transaction)
- **429 Too Many Requests**: Rate limiting exceeded

## Deployment

### Production Settings Checklist
1. **Environment Variables**: Set all required environment variables
2. **Debug Mode**: Set `DEBUG=False`
3. **Database**: Configure production PostgreSQL database
4. **Static Files**: Configure WhiteNoise for static file serving
5. **CORS**: Set appropriate ALLOWED_HOSTS and CORS settings
6. **SSL/HTTPS**: Configure SSL certificates and HTTPS redirects

### Environment Variables for Production
```env
# Core Django Settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-production-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-production-cloud-name
CLOUDINARY_API_KEY=your-production-api-key
CLOUDINARY_API_SECRET=your-production-api-secret

# Rate Limiting (optional)
THROTTLE_RATES={"otp": "5/hour", "transaction": "100/hour"}
```

### Using Gunicorn (Production)
```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run production server
gunicorn village_banking.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Or use Procfile for Heroku deployment
web: gunicorn village_banking.wsgi:application
```

### Database Migration in Production
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test user_accounts

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage (install coverage first)
pip install coverage
coverage run manage.py test
coverage report
```

### Test Coverage Areas
- User registration and authentication
- Transaction processing logic
- Admin dashboard functionality
- Permission and security testing
- API endpoint validation
- Database model constraints

## Contributing

We welcome contributions to the Village Banking System! Here's how to get started:

### Development Setup
1. **Fork the Repository**: Create your own fork on GitHub
2. **Clone Locally**: `git clone your-fork-url`
3. **Create Virtual Environment**: Follow installation instructions
4. **Install Dependencies**: `pip install -r requirements.txt`
5. **Set Up Database**: Run migrations and create test data

### Contribution Guidelines
1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Write Tests**: Add tests for new functionality
3. **Follow Code Style**: Maintain consistency with existing code
4. **Update Documentation**: Update README.md if needed
5. **Test Thoroughly**: Ensure all tests pass
6. **Submit Pull Request**: Provide clear description of changes

### Code Standards
- Follow Django best practices
- Use Django REST Framework conventions
- Write clear, self-documenting code
- Add docstrings for complex functions
- Maintain security standards

### Areas for Contribution
- **Frontend Development**: Create React/Vue.js frontend
- **Additional Payment Methods**: Integrate mobile money, cards
- **Reporting Features**: Advanced analytics and reporting
- **Mobile App**: Native mobile application
- **API Enhancements**: Additional filtering and search features
- **Performance Optimization**: Query optimization and caching

## Support & Maintenance

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Refer to this README and API documentation
- **Code Review**: Submit pull requests for community review

### Maintenance Notes
- **Regular Updates**: Keep dependencies updated for security
- **Backup Strategy**: Implement regular database backups
- **Monitoring**: Set up application monitoring and logging
- **Security Audits**: Regular security reviews and updates

## License

This project is licensed under the MIT License. See the LICENSE file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## Changelog

### Version 1.0.0 (Current)
- ✅ Complete user authentication system with JWT
- ✅ Multi-role support (User, Staff, Admin)
- ✅ Secure transaction processing (Deposit, Withdraw, Transfer)
- ✅ Admin dashboard with user and transaction management
- ✅ OTP-based password reset system
- ✅ Comprehensive API documentation
- ✅ Rate limiting and security features
- ✅ Cloudinary integration for image uploads
- ✅ Advanced filtering and search capabilities

### Planned Features (Version 2.0.0)
- 🔄 Real-time notifications
- 🔄 Transaction reports and analytics
- 🔄 Mobile application support
- 🔄 Multi-currency support
- 🔄 Integration with payment gateways
- 🔄 Loan management system

---

## Important Notes

⚠️ **Security Warning**: This is a community banking system designed for educational and village environments. For production deployment:

1. **Security Review**: Conduct thorough security auditing
2. **Compliance**: Ensure compliance with local banking regulations
3. **Backup Strategy**: Implement robust backup and disaster recovery
4. **Monitoring**: Set up comprehensive application monitoring
5. **Documentation**: Maintain updated security and operational documentation

🏦 **Banking Context**: This system is designed for village communities and cooperative banking scenarios. It provides essential banking operations while maintaining simplicity and security appropriate for community-level financial management.

📞 **Support**: For technical support, feature requests, or contributions, please use the GitHub repository's issue tracking system.
