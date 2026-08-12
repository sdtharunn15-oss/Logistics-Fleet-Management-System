Logistics & Fleet Management System

1. Project Overview

The Logistics & Fleet Management System is a backend application designed to manage and monitor vehicles, drivers, trips, fuel consumption, vehicle maintenance, GPS tracking records, authentication, and fleet reports.

The system is developed using Python and FastAPI and follows a structured backend architecture with separate layers for models, schemas, routers, services, utilities, and database management.

The primary objective of the system is to provide a centralized platform for managing fleet operations and maintaining accurate records of vehicles, drivers, trips, fuel usage, maintenance activities, and tracking information.

The application exposes RESTful APIs that can be accessed and tested through FastAPI Swagger documentation.


2. Project Objectives

The main objectives of this project are:

- Manage fleet vehicles and their current status.
- Manage driver information and availability.
- Manage trips assigned to vehicles and drivers.
- Prevent unavailable vehicles from being assigned to new trips.
- Track fuel consumption and fuel costs.
- Record vehicle maintenance activities.
- Store vehicle location and tracking information.
- Provide authentication and role-based access.
- Generate fleet-related reports.
- Maintain data consistency using database transactions.
- Provide reusable service-layer business logic.
- Validate request and response data using Pydantic.
- Provide automated testing using pytest.
- Provide API documentation through Swagger/OpenAPI.


3. Main Features

3.1 Authentication

The authentication module provides:

- User registration.
- User login.
- Password hashing.
- JWT access token generation.
- JWT token validation.
- Current-user information.
- User account activation status.
- Role-based authorization.

Supported roles:

- Admin
- Fleet Manager
- Driver

Passwords are not stored as plain text. Passwords are hashed using bcrypt through Passlib.


3.2 Vehicle Management

The vehicle module provides complete vehicle management functionality.

Features include:

- Create a vehicle.
- View all vehicles.
- View a vehicle by ID.
- Update vehicle information.
- Delete a vehicle.
- Prevent duplicate vehicle numbers.
- Maintain vehicle status.
- Prevent deletion of assigned vehicles.

Supported vehicle statuses:

- Available
- Assigned
- Maintenance
- Inactive

Important vehicle fields include:

- Vehicle number
- Vehicle type
- Model
- Manufacturing year
- Capacity
- Current kilometer reading
- Status


3.3 Driver Management

The driver module manages driver information.

Features include:

- Create driver.
- View all drivers.
- View driver by ID.
- Update driver.
- Delete driver.
- Prevent duplicate license numbers.
- Prevent duplicate email addresses.
- Track driver availability.

Driver information includes:

- Name
- License number
- Phone number
- Email
- Experience in years
- Availability status


3.4 Trip Management

The trip module manages fleet trips.

Features include:

- Create a trip.
- View all trips.
- View trip by ID.
- Update trip.
- Delete trip.
- Assign vehicles to trips.
- Assign drivers to trips.
- Track origin and destination.
- Track distance.
- Track trip status.

Supported trip statuses:

- planned
- in_progress
- completed
- cancelled

Business rules include:

- The selected vehicle must exist.
- The selected driver must exist.
- The vehicle must be Available before assigning it to a trip.
- Creating a trip changes the vehicle status to Assigned.
- Completing a trip makes the vehicle Available again.
- Cancelling a trip makes the vehicle Available again.
- Deleting an active trip releases the vehicle.


3.5 Fuel Management

The fuel module stores fuel consumption records for vehicles.

Features include:

- Create fuel record.
- View fuel records.
- View individual fuel records.
- Update fuel information.
- Delete fuel records.
- Calculate total fuel cost.
- Record odometer reading.
- Record fuel date.

Fuel information includes:

- Vehicle ID
- Fuel type
- Quantity in liters
- Price per liter
- Total cost
- Odometer reading
- Fuel date

The total fuel cost is calculated using the quantity and price per liter.


3.6 Maintenance Management

The maintenance module manages vehicle maintenance activities.

Features include:

- Create maintenance record.
- View maintenance records.
- View individual maintenance record.
- Update maintenance information.
- Delete maintenance records.
- Track maintenance status.
- Record maintenance cost.
- Record scheduled and completed dates.

Maintenance information includes:

- Vehicle ID
- Maintenance type
- Description
- Cost
- Status
- Maintenance date
- Completed date


3.7 Vehicle Tracking

The tracking module stores vehicle location information.

Features include:

- Create tracking record.
- View all tracking records.
- View tracking record by ID.
- Delete tracking record.
- Validate that the vehicle exists before creating a tracking record.

Tracking information includes:

- Vehicle ID
- Latitude
- Longitude
- Speed
- Recorded date and time


3.8 Reporting

The reporting module provides fleet-related reporting functionality.

Reports can be used to analyze information related to:

- Vehicles
- Drivers
- Trips
- Fuel
- Maintenance
- Orders and operational data available through the application

The report functionality is implemented separately from the API routing layer through a dedicated report service.


4. Technology Stack

Programming Language:

Python

Backend Framework:

FastAPI

Database ORM:

SQLAlchemy

Data Validation:

Pydantic

Authentication:

JWT

Password Hashing:

Passlib with bcrypt

Database:

SQLite is currently configured for the project.

Testing:

pytest

API Server:

Uvicorn

API Documentation:

Swagger UI / OpenAPI

Development Environment:

Python virtual environment


5. Project Architecture

The project follows a layered architecture.

The main layers are:

- Models
- Schemas
- Services
- Routers
- Utilities
- Database
- Configuration
- Tests


6. Project Structure

The project structure is organized approximately as follows:

logistics_fleet_management/

    app/

        __init__.py

        main.py

        config.py

        database.py

        models/
            __init__.py
            user.py
            vehicle.py
            driver.py
            trip.py
            fuel.py
            maintenance.py
            tracking.py

        schemas/
            __init__.py
            auth.py
            common.py
            driver.py
            fuel.py
            maintenance.py
            tracking.py
            trip.py
            vehicle.py

        services/
            __init__.py
            auth_service.py
            driver_service.py
            fuel_service.py
            maintenance_service.py
            report_service.py
            tracking_service.py
            trip_service.py
            vehicle_service.py

        routers/
            __init__.py
            auth.py
            driver.py
            fuel.py
            maintenance.py
            report.py
            tracking.py
            trip.py
            vehicle.py

        utils/
            __init__.py
            dependencies.py
            security.py

    tests/

        __init__.py
        test_auth.py
        test_drivers.py
        test_fuel.py
        test_maintenance.py
        test_tracking.py
        test_trips.py
        test_vehicles.py

    requirements.txt

    .env

    README.md


7. Models Layer

The models layer contains SQLAlchemy database models.

The main models are:

User

Stores authentication and user information.

Vehicle

Stores fleet vehicle information.

Driver

Stores driver information.

Trip

Stores trip assignments and trip information.

FuelRecord

Stores vehicle fuel records.

MaintenanceRecord

Stores vehicle maintenance records.

TrackingRecord

Stores vehicle GPS/location information.


8. Schemas Layer

The schemas layer contains Pydantic models used for request validation and response serialization.

Examples include:

UserRegister

Used for user registration.

UserLogin

Used for authentication.

UserResponse

Used to return user information.

VehicleCreate

Used to create vehicles.

VehicleUpdate

Used to update vehicles.

VehicleResponse

Used to return vehicle information.

DriverCreate

Used to create drivers.

DriverUpdate

Used to update drivers.

TripCreate

Used to create trips.

TripUpdate

Used to update trips.

FuelCreate

Used to create fuel records.

FuelUpdate

Used to update fuel records.

MaintenanceCreate

Used to create maintenance records.

MaintenanceUpdate

Used to update maintenance records.

TrackingCreate

Used to create tracking records.

TrackingResponse

Used to return tracking information.


9. Services Layer

The service layer contains the main business logic of the application.

The services are:

AuthService

Responsible for authentication-related operations.

VehicleService

Responsible for vehicle operations and vehicle validation.

DriverService

Responsible for driver operations and duplicate validation.

TripService

Responsible for trip assignment and vehicle availability logic.

FuelService

Responsible for fuel records and fuel cost calculation.

MaintenanceService

Responsible for maintenance records.

TrackingService

Responsible for vehicle tracking records.

ReportService

Responsible for fleet reporting functionality.

Keeping business logic in services makes the application easier to maintain and test.


10. Router Layer

The router layer exposes the application's REST API endpoints.

The routers communicate with the service layer and convert service exceptions into appropriate HTTP responses.

Main router modules include:

- Authentication router
- Vehicle router
- Driver router
- Trip router
- Fuel router
- Maintenance router
- Tracking router
- Report router


11. Database Configuration

The application uses SQLAlchemy for database interaction.

The database configuration is managed through the application settings.

SQLite is currently supported by the database configuration.

For SQLite, the application uses:

check_same_thread=False

This allows the database to be used correctly with the FastAPI application environment.

Database sessions are created through SQLAlchemy's sessionmaker.

The get_db dependency provides database sessions to API endpoints and closes the session after the request is completed.


12. Environment Configuration

Configuration values are stored using environment variables.

A typical .env file can contain values similar to:

DATABASE_URL=sqlite:///./fleet_management.db

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

The actual secret key should be replaced with a strong secret value in a real deployment.

Do not commit sensitive environment variables or production secrets to a public repository.


13. Authentication Flow

The authentication process works as follows:

1. A user registers using the registration endpoint.
2. The password is validated using Pydantic.
3. The password is hashed before being stored.
4. The user is stored in the database.
5. The user logs in using email and password.
6. The password is verified against the stored hash.
7. A JWT access token is generated.
8. The client sends the token with protected requests.
9. The authentication dependency decodes the token.
10. The user ID is extracted from the token.
11. The user is loaded from the database.
12. The user's active status is checked.
13. The authenticated user is returned to the endpoint.


14. Role-Based Authorization

The application supports role-based authorization.

Available roles:

Admin

Fleet Manager

Driver

The require_roles dependency can be used to restrict endpoints to specific roles.

If a user does not have the required role, the application returns:

HTTP 403 Forbidden

with an insufficient permissions message.


15. API Documentation

FastAPI automatically generates OpenAPI documentation.

After starting the application, Swagger UI is available at:

http://127.0.0.1:8000/docs

The alternative ReDoc documentation is available at:

http://127.0.0.1:8000/redoc

The Swagger interface can be used to:

- View available endpoints.
- View request schemas.
- View response schemas.
- Test API endpoints.
- Authenticate using JWT.
- Check HTTP responses.


16. Installation

Step 1: Clone or copy the project.

Step 2: Open the project directory:

cd logistics_fleet_management

Step 3: Create a virtual environment:

python -m venv venv

Step 4: Activate the virtual environment on Windows PowerShell:

venv\Scripts\Activate.ps1

Step 5: Install dependencies:

pip install -r requirements.txt


17. Running the Application

Start the FastAPI application using:

uvicorn app.main:app --reload

The application will normally be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs


18. Running Tests

The project uses pytest for automated testing.

Run the complete test suite:

pytest -v

Run a specific test file:

pytest tests\test_vehicles.py -v

Run driver tests:

pytest tests\test_drivers.py -v

Run trip tests:

pytest tests\test_trips.py -v

Run fuel tests:

pytest tests\test_fuel.py -v

Run maintenance tests:

pytest tests\test_maintenance.py -v

Run tracking tests:

pytest tests\test_tracking.py -v

Run authentication tests:

pytest tests\test_auth.py -v


19. Python Compilation Check

Python compilation can be checked using:

python -m compileall app

This verifies that Python files can be compiled successfully and helps identify syntax errors before running the application.


20. Testing Strategy

The project contains tests for the major service modules.

Authentication tests cover:

- User registration.
- Supported roles.
- Duplicate email.
- Authentication.
- Invalid password.
- Invalid email.
- Inactive user.
- JWT token creation.
- JWT token payload.

Vehicle tests cover:

- Vehicle creation.
- Duplicate vehicle number.
- Vehicle retrieval.
- Vehicle update.
- Vehicle deletion.
- Vehicle status validation.
- Protection of assigned vehicles.

Driver tests cover:

- Driver creation.
- Duplicate license number.
- Duplicate email.
- Driver retrieval.
- Driver update.
- Driver deletion.

Trip tests cover:

- Trip creation.
- Vehicle validation.
- Driver validation.
- Vehicle availability.
- Vehicle assignment.
- Trip status updates.
- Trip completion.
- Trip cancellation.
- Trip deletion.
- Vehicle release.

Fuel tests cover fuel record creation and fuel-related operations.

Maintenance tests cover maintenance record operations.

Tracking tests cover:

- Tracking record creation.
- Vehicle validation.
- Tracking retrieval.
- Tracking deletion.
- Default speed handling.
- Missing tracking records.

The tests use isolated SQLite databases where required to avoid modifying production application data.


21. Vehicle Assignment Business Logic

Vehicle availability is an important part of the fleet system.

When a trip is created:

Available vehicle

becomes:

Assigned vehicle

When the trip is completed:

Assigned vehicle

becomes:

Available vehicle

When the trip is cancelled:

Assigned vehicle

becomes:

Available vehicle

When an active trip is deleted:

Assigned vehicle

becomes:

Available vehicle

This prevents the same vehicle from being assigned to multiple active trips.


22. Error Handling

The application uses FastAPI HTTP exceptions at the API layer and service-level exceptions for business rules.

Common HTTP responses include:

200 OK

The request was completed successfully.

201 Created

A new resource was successfully created.

400 Bad Request

The request violates a business rule or contains invalid data.

401 Unauthorized

Authentication failed or the JWT token is invalid or expired.

403 Forbidden

The authenticated user does not have permission or the account is inactive.

404 Not Found

The requested resource does not exist.

422 Unprocessable Entity

The request failed Pydantic validation.


23. Data Validation

Pydantic schemas validate incoming request data before it reaches the business logic.

Examples of validation include:

- Required fields.
- Minimum and maximum string lengths.
- Email validation.
- Password length.
- Manufacturing year range.
- Positive vehicle capacity.
- Non-negative kilometer values.
- Numeric fuel values.
- Valid request structures.

This helps prevent invalid data from entering the database.


24. Security

The application includes several security measures:

- Password hashing using bcrypt.
- JWT-based authentication.
- Token expiration.
- Protected endpoints.
- Role-based authorization.
- Active-user verification.
- Request validation.
- Database session management.

Production deployments should additionally use:

- HTTPS.
- Strong secret keys.
- Secure environment variables.
- Production-grade database configuration.
- Proper CORS configuration.
- Secure logging.
- Rate limiting where required.


25. Example Authentication Flow

Register a user:

POST /auth/register

Example request:

{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "Admin@123",
    "role": "Admin"
}

Login:

POST /auth/login

Example request:

{
    "email": "admin@example.com",
    "password": "Admin@123"
}

The response contains:

{
    "access_token": "JWT_TOKEN",
    "token_type": "bearer"
}

The token can then be used to access protected endpoints.


26. Example Vehicle

Example vehicle request:

{
    "vehicle_number": "TN01AB1234",
    "vehicle_type": "Truck",
    "model": "Tata 407",
    "manufacturing_year": 2022,
    "capacity": 5000,
    "current_km": 10000
}

The newly created vehicle is initially assigned:

status = "Available"


27. Example Driver

Example driver request:

{
    "name": "Arun Kumar",
    "license_number": "TN-DL-12345",
    "phone": "9876543210",
    "email": "arun@example.com",
    "experience_years": 5,
    "is_available": true
}


28. Example Trip

Example trip request:

{
    "vehicle_id": 1,
    "driver_id": 1,
    "origin": "Chennai",
    "destination": "Bangalore",
    "distance_km": 350,
    "status": "planned"
}

Creating the trip changes the selected vehicle status from:

Available

to:

Assigned


29. Example Fuel Record

Example fuel request:

{
    "vehicle_id": 1,
    "fuel_type": "diesel",
    "quantity_liters": 100,
    "price_per_liter": 95,
    "odometer": 10500
}

The fuel service calculates the total fuel cost based on the quantity and price per liter.


30. Example Maintenance Record

Example maintenance request:

{
    "vehicle_id": 1,
    "maintenance_type": "Engine Service",
    "description": "Regular engine maintenance",
    "cost": 5000,
    "status": "scheduled"
}


31. Example Tracking Record

Example tracking request:

{
    "vehicle_id": 1,
    "latitude": 13.0827,
    "longitude": 80.2707,
    "speed": 45
}


32. Recommended Demonstration Flow

For a project demonstration, the following sequence provides a complete end-to-end workflow:

Step 1

Open Swagger documentation.

Step 2

Register an Admin or Fleet Manager account.

Step 3

Login and obtain the JWT access token.

Step 4

Authorize Swagger using the JWT token.

Step 5

Create a vehicle.

Step 6

Create a driver.

Step 7

Create a trip using the vehicle and driver.

Step 8

Show that the vehicle status changes to Assigned.

Step 9

Create a fuel record for the vehicle.

Step 10

Create a maintenance record.

Step 11

Create a tracking record.

Step 12

Complete or cancel the trip.

Step 13

Show that the vehicle status becomes Available again.

Step 14

Open the report endpoints and demonstrate the available fleet information.

Step 15

Show the automated pytest results.


33. Development Validation Checklist

Before final submission, verify:

- Application starts successfully.
- Swagger documentation opens.
- Database connection works.
- User registration works.
- User login works.
- JWT authentication works.
- Role validation works.
- Vehicle CRUD works.
- Driver CRUD works.
- Trip operations work.
- Vehicle assignment works.
- Vehicle release works.
- Fuel operations work.
- Maintenance operations work.
- Tracking operations work.
- Report endpoints work.
- Invalid requests return appropriate errors.
- Complete pytest suite passes.
- Python compilation succeeds.


34. Production Considerations

This project is structured as a backend application and can be extended for production use.

Possible future improvements include:

- PostgreSQL production database.
- Redis caching.
- Background task processing.
- Celery integration.
- Real-time GPS tracking.
- WebSocket-based tracking.
- Advanced fleet analytics.
- Driver performance analytics.
- Fuel efficiency calculations.
- Maintenance reminders.
- Automated notifications.
- Email notifications.
- Docker deployment.
- CI/CD pipeline.
- Cloud deployment.
- Centralized logging.
- Monitoring and alerting.


35. Benefits of the System

The Logistics & Fleet Management System provides a centralized backend for fleet operations.

The system helps organizations:

- Maintain accurate vehicle records.
- Manage drivers efficiently.
- Control vehicle assignments.
- Track trips.
- Monitor fuel usage.
- Record maintenance activities.
- Store vehicle tracking data.
- Control user access.
- Generate operational reports.
- Reduce manual record keeping.
- Improve fleet visibility.


36. Conclusion

The Logistics & Fleet Management System provides a structured FastAPI backend for managing core fleet operations.

The application separates database models, validation schemas, business services, API routers, authentication utilities, and automated tests.

The service-oriented structure makes the project easier to maintain, test, extend, and integrate with future frontend or mobile applications.

The current implementation provides the foundation for vehicle management, driver management, trip management, fuel management, maintenance management, tracking, authentication, authorization, and reporting.

The system can be further extended with production database support, real-time tracking, background processing, analytics, notifications, and cloud deployment.
