# custom_user_auth (Task-Backend-1)
## Project Deployment and Swagger UI Access

I'm excited to announce that the project has been successfully deployed on a hosting platform and is now accessible for use. You have two convenient options to explore the project's capabilities:

1. **Access the Deployed Project:**
_All features have been tested and are working seamlessly using the Swagger UI interface._
   You can access the project through the Swagger UI interface, which provides a user-friendly way to interact with the project's APIs. Simply navigate to the provided Swagger UI link:

   - Hosting Platform: [PythonAnywhere](https://www.pythonanywhere.com/)
   - Accessible Swagger UI: [Swagger UI Link](https://nematulloh.pythonanywhere.com/swagger/)

   Alternatively, you can also explore the API documentation using Redoc, another intuitive tool for API visualization:

   - Accessible Redoc: [Redoc Link](https://nematulloh.pythonanywhere.com/redoc/)

   From both the Swagger UI and Redoc interfaces, you can explore the available APIs, endpoints, and functionalities with ease. It's a great way to test, develop, or interact with the project.


3. **Access APIs Individually:**
   If you're interested in specific API endpoints, you can also access them directly by using their respective URLs. This is a handy option if you want to quickly test or integrate specific functionalities.
The project offers a variety of API endpoints that you can access to perform specific actions. Instead of using the Swagger interface, you can directly interact with these APIs by using their respective paths. Below, you'll find a list of available endpoints along with brief descriptions of their functionalities:

1. **Register User:**
   - URL: `/api/register/`
   - Description: Register a new user account.

2. **User Login:**
   - URL: `/api/login/`
   - Description: Log in to your user account.

3. **Verify OTP:**
   - URL: `/api/verify/`
   - Description: Verify your account using a one-time password (OTP).

4. **User Profile:**
   - URL: `/api/profile/`
   - Description: Retrieve your user profile information.

5. **Update Profile:**
   - URL: `/api/update/`
   - Description: Update your user profile information.

6. **User Logout:**
   - URL: `/api/logout/`
   - Description: Log out from your user account.

7. **Delete User:**
   - URL: `/api/delete/`
   - Description: Delete your user account.


To access these API endpoints directly, simply append the provided URLs to the base API path: `https://nematulloh.pythonanywhere.com/api/`. For instance, to register a new user, you can make a POST request to `https://nematulloh.pythonanywhere.com/api/register/`.


Best regards,
Ne'matulloh

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


## Configuring Celery with Redis
### Note: OTP Printing for Celery Debugging

During the testing phase, if you encounter any issues with the Celery tasks related to OTP verification, the one-time password (OTP) will be printed in the terminal. You have the option to use the project even without configuring this feature.

If your Django project requires asynchronous task processing using Celery and you want to configure it with Redis as the message broker on your local machine, follow these steps:

1. **Install and Set Up Redis:**

   - For Windows:
     - Download the Redis for Windows executable from the GitHub repository: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
     - Download Redis-x64-3.0.504.msi and connect to port 6379
     

   - For Other Operating Systems:
     - Follow the official Redis installation guide for your operating system: [https://redis.io/download](https://redis.io/download)

   

2. **Install Celery And Redis:**
- In your project's virtual environment, install Celery using pip:
  ```
  pip install celery
  pip install redis
  ```

### Changing Email and Password for Sending Emails

1. **Access Django Project Settings:**
   Open your Django project's `settings.py` file. This file contains all the configuration settings for your project.

2. **Locate Email Configuration:**
   Find the section in your `settings.py` file where the email configuration settings are defined. This is the block of code you provided earlier:

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

If you've developed a Django backend application and want to deploy it on PythonAnywhere while also configuring static file mappings, follow these steps:

1. **Log In/Create Account:**
   - If you don't have a PythonAnywhere account, sign up for one at [https://www.pythonanywhere.com/registration/register/beginner/](https://www.pythonanywhere.com/registration/register/beginner/).

2. **Create a Web App:**
   - After logging in, navigate to the Dashboard.
   - Click on "Web" to create a new web app.
   - Choose "Manual Configuration" and select the appropriate Python version.

3. **Clone Your Repository:**
   - From your Dashboard, navigate to the "Files" section.
   - Clone your backend application's repository using Git:
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

8. **Database Configuration:**
   - If your application uses a database, configure the database settings in your application and the PythonAnywhere database section.

9. **Restart Web App:**
   - Go back to the "Web" section and click the "Reload" button to apply your changes.
   - Your deployed backend application should be live on the provided URL.

10. **Monitor and Debug:**
    - Check the "Errors" and "Server Logs" sections on PythonAnywhere for any issues or errors.
    - Test your deployed backend application to ensure it functions as expected.

By following these steps, you'll successfully deploy your Django backend application on PythonAnywhere and configure static file mappings for your project.


## Conclusion

Thank you for your interest in exploring this project. I hope this README has provided you with a clear understanding of the deployment process and how to interact with the project's APIs. Feel free to access the deployed project through the provided links and explore its functionalities.

If you're looking for further assistance, have questions, or want to discuss any aspect of this project, I'm always available on Telegram:

**Telegram:** [@nematulloh_uktamov](https://t.me/nematulloh_uktamov)

Best regards and good luck on your journey with this project!

Ne'matulloh


