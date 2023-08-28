# custom_user_auth
# Your DRF Backend Application

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

pip install -r requirements.txt


6. **Apply Migrations:**

python manage.py makemigrations
python manage.py migrate


7. **Create a Superuser (Optional):**

```
python manage.py createsuperuser
```


8. **Run the Development Server:**

```
python manage.py runserver
```

9. **Access the Application:**

Open your web browser and visit `http://127.0.0.1:8000/`.

## Additional Configuration

- **Authentication Token:** Token-based authentication is configured. Update `AUTH_USER_MODEL` in `config/settings.py`.

- **Celery Configuration:** Update Celery-related configurations in `config/settings.py` if using Celery.

- **Email Configuration:** Configure email settings in `config/settings.py` for sending emails.

- **Cache Configuration:** Configure cache settings in `config/settings.py`.


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
