# import os

# os.system('python manage.py makemigrations --noinput')
# os.system('python manage.py migrate --noinput')

import subprocess

try:
    # Run makemigrations
    subprocess.run(['python', 'manage.py', 'makemigrations', '--noinput'], check=True)
    # Run migrate
    subprocess.run(['python', 'manage.py', 'migrate', '--noinput'], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

# import subprocess
# import os

# try:
#     # Run makemigrations
#     subprocess.run(['python', 'manage.py', 'makemigrations', '--noinput'], check=True)
#     # Run migrate
#     subprocess.run(['python', 'manage.py', 'migrate', '--noinput'], check=True)

#     # Environment variables for superuser creation
#     os.environ['DJANGO_SUPERUSER_USERNAME'] = 'Admin'        # Replace with your desired username
#     os.environ['DJANGO_SUPERUSER_EMAIL'] = 'admin@gmail.com'  # Replace with your desired email
#     os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'Bitek_Admin'     # Replace with your desired password

#     # Run createsuperuser command non-interactively
#     subprocess.run(
#         ['python', 'manage.py', 'createsuperuser', '--noinput'],
#         check=True
#     )
#     print("Superuser created successfully.")

# except subprocess.CalledProcessError as e:
#     print(f"An error occurred: {e}")

