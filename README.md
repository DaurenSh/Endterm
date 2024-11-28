Warehouse accounting CRM
		
Main system functionality

User registration and authentication:
Users can register in the system, create accounts with data (name, email, password, phone, role).
A JWT token is used for authentication.

Product management:
Administrators can add, edit and delete product information, including name, description, price, quantity and points.
Products are classified by category.

Transactions:
The system takes into account transactions for the receipt and issue of products. Users can perform transactions through the API.
Transaction information includes type (reception or issue), quantity and product.

Reports:
Daily reports: The system generates product reports for each day, showing the number of received and issued goods.
Monthly reports: A monthly report is generated based on daily reports, providing a more complete picture for the month.

Analytics:
Users can get analytical information on the movement of products for a selected period using graphs and charts.

User roles:
Division into roles (e.g. administrator, warehouse employee) to ensure the appropriate level of access.
Interfaces and technologies
Backend: Django (for creating web application and API).
Frontend: Using HTML, CSS, Bootstrap, JavaScript.
API: REST API implemented with Django REST Framework and drf-spectacular for generating documentation.
Authentication: JWT via Django REST Framework Simple JWT.

Api Documentation
POST /auth/jwt/create/ -- Obtaining JWT tokens for user authentication
Example:
{
    "username": "john_doe",
    "password": "securepassword123"
}

GET /api/products/ -- Getting a list of all products.
POST /api/products/ -- Create a new product (for administrators only).
Example:
{
    "name": "Smartphone",
    "description": "Latest model smartphone with high performance",
    "price": 999.99,
    "quantity": 50,
    "pv_points": 200,
    "category": 1
}

GET /api/transactions/ -- Get a list of all transactions.
POST /api/transactions/ -- Create a new transaction.
{
    "transaction_type": "acceptance",
    "product": 1,
    "quantity": 20,
    "responsible_user": 2
}


GET /api/daily-reports/ -- Get a list of daily reports
POST /api/daily-reports/ -- Create a new daily report.
Example:
{
    "date": "2024-11-19",
    "category": 1,
    "total_products_received": 50,
    "total_products_issued": 30,
    "report_generated_by": 2
}

GET /api/monthly-reports/ -- Get a list of monthly reports.
POST /api/monthly-reports/ -- Creating a new monthly report.
Example:
{
    "date": "2024-11-01",
    "category": 1,
    "total_products_received": 150,
    "total_products_issued": 120,
    "report_generated_by": 2
}

POST /auth/users/ -- Creating a new user.
Example:
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": 1,
    "phone_number": "+123456789"
}

Starting Redis
docker exec -it redis_server redis-cli
select 1
