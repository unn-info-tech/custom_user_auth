# custom_user_auth 


## Introduction
This project implements Custom User RESTful APIs with token-based Authentication and Authorization, utilizing Django Rest Framework (DRF) for seamless management of various user-related operations.


### Features:
- User Registration
- User Login
- OTP Verification
- Profile Management
- Logout
- Account Deletion

### Used Technologies:

- **Framework:** Django
- **API Development:** Django Rest Framework (DRF)
- **Task Management:** Celery
- **Asynchronous Broker:** Redis
- **Email Integration:** SMTP (Gmail)
- **Hosting Platform:** PythonAnywhere


### Gained Experience and Skills

Throughout this project, I've acquired an array of skills and hands-on experience in backend development, deployment, and security practices.
Here's a summary of what I've learned:

- **Django & Django Rest Framework (DRF):** Developed robust RESTful APIs, managing authentication, user registration, and profiles efficiently.

- **Database Operations:** Executed migrations, managed data models, and administered backend using Django's ORM.

- **Celery and Redis Integration:** Implemented asynchronous tasks, particularly for OTP (one-time password) sending via email.

- **Email Integration in Django:** Configured email settings and security measures using SMTP, integrated with Gmail for secure communication.

- **Deployment (PythonAnywhere):** Deployed Django apps, handled static files, and configured web apps on hosting platforms.

- **Best Practices:** Adhered to coding standards, documentation, and project organization best practices.

- **Debugging & Monitoring:** Proficient in identifying and resolving deployment issues through log monitoring and error debugging.

- **Security Practices:** Implemented token-based authentication, managed sensitive data securely, and created custom user models for enhanced security.

- **API Design & Documentation:** Developed comprehensive API documentation using Swagger UI and Redoc, ensuring clear endpoint descriptions and authentication mechanisms.

This experience has enriched my knowledge in backend development, deployment strategies, and security practices.

## Access the Deployed Project

The project is now live on a hosting platform, offering accessible usage through two options:

1. **Explore via Swagger UI and Redoc:**
   Access the project's functionalities seamlessly using [Swagger UI(link)](https://nematulloh.pythonanywhere.com/swagger/) and [Redoc(link)](https://nematulloh.pythonanywhere.com/redoc/)
   #### Usage:
   - Register: Begin by registering a new user account.
   - Login: Log in with your registered account using your email and password. After providing your email and password, verify the OTP you receive to obtain the authentication token.
   - Profile Management: Fetch your user profile and update your profile information(using the authentication token).
   - Logout: Log out from the current session(using the authentication token).
   - Account Deletion: Delete your user account, if needed(using the authentication token).

3. **Direct API Access:**
   Interact with specific API endpoints by appending them to the base API path:
   - `/api/register/`
   - `/api/login/`
   - `/api/verify/`
   - `/api/profile/`
   - `/api/update/`
   - `/api/logout/`
   - `/api/delete/`

To access these API endpoints directly, simply append the provided URLs to the base API path: `https://nematulloh.pythonanywhere.com/api/`. For instance, to register a new user, you can make a POST request to `https://nematulloh.pythonanywhere.com/api/register/`.

# Try It on Your Local Machine:
   If you prefer to test the project on your local machine, you can follow these steps:

This guide provides step-by-step instructions to set up and deploy your Django (DRF) backend application.

## Prerequisites

- Python (3.6 or higher)
- Django(DRF)
- Virtual Environment 

## Getting Started

1. **Clone the Repository:**

```
git clone <repository_url>
cd <project_directory>
```


2. **Create and Activate a Virtual Environment:**

```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. **Install Project Dependencies:**

```
pip install -r requirements.txt
```

6. **Apply Migrations:**

```
python manage.py makemigrations
python manage.py migrate
```

7. **Create a Superuser (Optional):**

```
python manage.py createsuperuser
```


8. **Run the Development Server:**

```
python manage.py runserver
```


## Configuring Celery with Redis for sending OTP to your email
**Note: OTP Printing for Celery Debugging**
During the testing phase, if you encounter any issues with the Celery tasks related to OTP verification, the one-time password (OTP) will be printed in the terminal. You have the option to use the project even without configuring this feature.


1. **Install and Set Up Redis:**

   - For Windows:
     - Download the Redis for Windows executable from the GitHub repository: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
     - Download Redis-x64-3.0.504.msi and connect to port 6379
     

   - For Other Operating Systems:
     - Follow the official Redis installation guide for your operating system: [https://redis.io/download](https://redis.io/download)

   

2. **Install Celery And Redis:**
- In your project's virtual environment, install Celery and Redis using pip:
  ```
  pip install celery
  pip install redis
  ```

### Changing Email and Password for Sending Emails

1. **Access Django Project Settings:**
   Open your Django project's `settings.py` file. This file contains all the configuration settings for your project.

2. **Locate Email Configuration:**
   Find the section in your `settings.py` file where the email configuration settings are defined. 

   ```python
   # Configuration for sending emails
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = "smtp.gmail.com"
   EMAIL_USE_TLS = True
   EMAIL_PORT = 587
   EMAIL_HOST_USER = "your_email@example.com"
   EMAIL_HOST_PASSWORD = "your_app_password"


3. **Change Email Address:**
   Replace `"your_email@example.com"` with the new Gmail email address you want to use for sending emails.

4. **Change App Password:**
   Replace `"your_app_password"` with the new app-specific password generated by Gmail for your account. If you haven't generated an app password before, you can follow these steps to create one:

   - Go to your Google Account settings: [https://myaccount.google.com/](https://myaccount.google.com/)
   - Under the "Security" section, locate the "App passwords" option.
   - Generate a new app password for your Django project. Select "Other (Custom name)" as the app and provide a name like "Django Email App."
   - Google will generate a unique app-specific password for your project. Use this password in the `EMAIL_HOST_PASSWORD` field.

3. **Save Changes:**
   After updating the email configuration settings, save the changes to your `settings.py` file.


4. **Create and Run Celery Worker:**
   - Open another terminal window and navigate to your project's directory.
   - Run the Celery worker:
     ```
     celery -A config worker -l info
     ```



## Deploying a Django Backend Application and Configuring Static Files on PythonAnywhere


1. **Log In/Create Account:**
   - If you don't have a PythonAnywhere account, sign up for one at [https://www.pythonanywhere.com/registration/register/beginner/](https://www.pythonanywhere.com/registration/register/beginner/).

2. **Create a Web App:**
   - After logging in, navigate to the Dashboard.
   - Click on "Web" to create a new web app.
   - Choose "Manual Configuration" and select the appropriate Python version.

3. **Clone Your Repository:**
   - From your Dashboard, navigate to the "Console" section.
   - Clone your backend application's repository using Git Bash:
     ```
     git clone [repository_url]
     ```

4. **Set Up Virtual Environment:**
   - In the terminal, navigate to your project directory:
     ```
     cd [project_directory]
     ```
   - Create a virtual environment:
     ```
     virtualenv venv --python=python3.8
     ```
   - Activate the virtual environment:
     ```
     source venv/bin/activate
     ```

5. **Install Dependencies:**
   - Install the required dependencies for your backend application using pip:
     ```
     pip install -r requirements.txt
     ```

6. **Configure WSGI File:**
   - Navigate to the "Web" section of PythonAnywhere.
   - Edit the WSGI configuration file and specify the path to your application's WSGI file.

7. **Configure Static Files:**
   - Scroll down to the "Static files" section.
   - Specify the URL path and directory of your static files.
   - In the terminal run the following command:
     ```
     python manage.py collectstatic
     ```

8. **Database Configuration:**
   - No need, because we are using Django's default DB

9. **Restart Web App:**
   - Go back to the "Web" section and click the "Reload" button to apply your changes.
   - Your deployed backend application should be live on the provided URL.

10. **Monitor and Debug:**
    - Check the "Errors" and "Server Logs" sections on PythonAnywhere for any issues or errors.
    - Test your deployed backend application to ensure it functions as expected.

By following these steps, you'll successfully deploy your Django backend application on PythonAnywhere and configure static file mappings.

## Conclusion

Thank you for your interest in exploring this project. I hope this README has provided you with a clear understanding of the deployment process and how to interact with the project's APIs. Feel free to access the deployed project through the provided links and explore its functionalities.

If you're looking for further assistance, have questions, or want to discuss any aspect of this project, I'm always available on Telegram:

**Telegram:** [@nematulloh_uktamov](https://t.me/nematulloh_uktamov)

Best regards and good luck on your journey with this project!

Ne'matulloh


