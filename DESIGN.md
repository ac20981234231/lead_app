## Overview

This document explains the design choices for the Lead Management Application, which collects lead information and sends email notifications to both the prospect and an internal attorney.

## Design Choices

### Framework: FastAPI
- **High Performance:** Offers excellent performance for asynchronous operations.
- **Developer-Friendly:** Automatic data validation and serialization with Pydantic models
- **Built-in Documentation:** Provides interactive API docs using Swagger and ReDoc. Great for both development and testing.

### ORM: SQLAlchemy
- **Robust ORM:** Simplifies database interactions.
- **Flexibility:** Supports complex queries, suitable for various app needs.
- **Clean Code:** Encourages maintainable codebase with its concise syntax.

### Database: SQLite
- **Simple and Lightweight:** Ideal for local dev since it doesn't require a separate server.
- **Quick Setup:** No configs needed => allowing for fast development and testing.
- **Easily Upgradable:** Can be replaced for a more robust database like PostgreSQL (i.e when moving to production).

### Email Notifications
- **Immediate Communication:** Ensures both prospect and attorney are promptly informed of new lead submissions.
- **Standard Library:** Uses `smtplib` for sending emails, avoiding extra dependencies.

### Environment Variables
- **Security:** Keeps sensitive information like email credentials out of the codebase.
- **Ease of Configuration:** Allows for quick setting updates without changing code.

### Directory Structure
- **Separation of Concerns:** Organizes the code into different directories for models, schemas, CRUD operations, database configuration, and the main logic.
- **Scalability:** Simpler to add new features and maintain codebase.

## Implementation Details

### Lead Submission

**Endpoint:** `POST /leads`
- **Functionality:** Accepts lead information (first name, last name, email, resume) and stores in DB. Sends email notifications to both prospect and attorney.

### Reading Leads

**Endpoint:** `GET /leads`
- **Functionality:** Retrieves a list of leads from DB. Meant for internal use and should be protected by authentication in a production environment.

### Updating Lead State

**Endpoint:** `PUT /leads/{lead_id}/state`
- **Functionality:** Updates the state of a lead to indicate it has been contacted. Assists in tracking the status of each lead.

## Time Management
Due to a busy schedule at work, I prioritized core functionalities and code quality, focusing on delivering a functional and well-documented application within the available time.


## Future Improvements

1. **Authentication and Authorization:**
   - Implement security measures to ensure only authorized personnel can access and modify lead information.

2. **Database Migration Tools:**
   - Use Alembic or similar tools to manage database migrations and maintain schema consistency across different environments.

3. **Enhanced Error Handling:**
   - Improve error handling and logging to better capture and address issues.

4. **Testing:**
   - Add unit and integration tests to ensure the application functions correctly and to support future development.

5. **Deployment Considerations:**
   - Configure the application for deployment with a robust database like PostgreSQL and set up a secure environment for managing secrets and configurations.

## Conclusion

The app is designed for performance, simplicity, and maintainability. FastAPI and SQLAlchemy provide a scalable foundation. SQLite is used for easy local development, while email notifications ensure timely communication. Environment variables enhance security. Future improvements aim to further secure and enhance the application for production.
