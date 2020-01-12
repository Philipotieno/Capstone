# Coffee Shop Backend

## Getting Started

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - can   - `get:actors`
                - `get:movies`
    - Casting Director
        - can   - `get:actors`
                - `post:actors`
                - `patch:actors`
                - `delete:actors`
                - `get:movies`
                - `patch:movies`
    - Executive Producer
        - can   - `get:actors`
                - `get:movies`
                - `post:movies`
                - `delete:movies`
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users and assign them the three roles 
            User 1 - Casting Assistant
            User 2 - Casting Director
            User 3 - Executive Producer
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for Casting Assistant, Casting Director, and Executive Producer
    - Navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).

### Create Database
```
    $ sudo su postgres
    $ psql`
    postgres=# CREATE DATABASE capstone;
    postgres=# CREATE DATABASE capstone_test;`
    postgres=# \q
    $ exit

```
### Installing Dependencies

#### Python 3.6

To run the server, execute:

```bash
- Then add a .env file as shown in the following sample
  ```
  - `source venv/bin/activate`

  - `export FLASK_APP="run.py"`
  - `export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"`
  - `export APP_SETTINGS="development"`

  - `export DATABASE_URL="postgres://mitch:mufasa2019@localhost/capstone"`
  - `export TESTDB_URL="postgres://mitch:mufasa2019@localhost/capstone_test"`

  - `export AUTH0_DOMAIN="domain.auth0.com"`
  - `export API_AUDIENCE="your api audience"`
  ```

### To Create and activate the virtual environment
```
    $ virtualenv -p python3 venv
    $ pip install -r requirements.txt
    $ source .env
```
### To Run migrations
```
    $ python manage.py db init
    $ python manage.py db migrate
    $ exit

```
### To run the app
```
$ flask run --reload
```
## To run tests
```
$ python test_app.py
```
## Endpoints...

### POST '/actors'

- Adds a new actor
- Request Arguments: Question body

```
- Actors body: 

```json5
{
    "age": 16,
    "gender": "Male",
    "id": 50,
    "name": "Ptte Dfd"
}
```
- Returns: 

```json5
{
    "actors": [
        {
            "age": 16,
            "gender": "Male",
            "id": 50,
            "name": "Ptte Dfd"
        }
    ],
    "success": true
}
```