# User CRUD Project

## Steps to Run the Project:

1. Create a virtual env and Run the following command to install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. After installing dependencies, run the following command to start the server:
    ```
    python manage.py runserver
    ```

3. Visit [localhost:8000/swagger](http://localhost:8000/swagger) to open the Swagger interface where you can test the APIs.

4. First, call the `/token` API using the credentials (username='user2', password='user2'). This will return the access token, which you can copy.

5. Open the lock icon on the right side to authenticate. Paste the "Bearer {access_token}" you just copied.

6. You can now test the APIs.
