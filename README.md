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
    ```
        GET https://YOUR_DOMAIN/authorize?
            audience=YOUR_AUDIENCE&
            response_type=token&
            client_id=YOUR_CLIENT_ID&
            redirect_uri=https://callbackurl&

    ```
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
- Authorization required: Casting Director
- Request Arguments: Actors body

```
- Actors body: 

{
    "name": "Brad Pitt",
    "age": 56,
    "gender": "Male"
}
```
- Returns: 

```json5
{
    "actors": [
        {
            "age": 16,
            "gender": "Male",
            "id": 56,
            "name": "Brad Pitt"
        }
    ],
    "success": true
}
```
### GET '/actors'

- Fetches a dictionary of all actors
- Authorisation required: Casting Assistant/Casting Director/Executive Producer
- Returns: 

```json5
{
    "actors": [
        {
            "age": 65,
            "gender": "Male",
            "id": 2,
            "name": "Brad"
        },
        {
            "age": 65,
            "gender": "Male",
            "id": 1,
            "name": "Jim Carrey"
        }
    ],
    "success": true
}
```

### GET '/actors/1'

- Fetches a dictionary of one actor
- Authorization required: Casting Assistant/Casting Director/Executive Producer
- Returns: 

```json5
{
    "actor": {
        "age": 65,
        "gender": "Male",
        "id": 1,
        "name": "Jim Carrey"
    },
    "success": true
}
```

### DELETE '/actors/1'

- Deletes an actor
- Authorization required: Casting Director
- Returns: 

```json5
{
    "deleted": 2,
    "success": true
}
```
### PATCH '/actors/1'

- update actors name
- Authorization required: Casting Director
- Request Arguments: Actors body

```
- Actors body: 

```json5
{
    "name": "Brad Pitt Jr",
    "age": 56,
    "gender": "Male"
}
```
- Returns: 

```json5
{
    "actors": [
        {
            "age": 16,
            "gender": "Male",
            "id": 56,
            "name": "Brad Pitt Jr"
        }
    ],
    "success": true
}
```



### POST '/movies'

- Adds a new movies
- Authorization required: Executive Producer
- Request Arguments: movies body

```json
{
    "title": "Mad Max",
    "release_date": "5-6-2020"
}
```
- Returns: 

```json5
{
    "movie": [
        {
            "id": 14,
            "release_date": "Sat, 02 Feb 3202 00:00:00 GMT",
            "title": "Dark Night"
        }
    ],
    "success": true
}
```
### GET '/actors'

- Fetches a dictionary of all movies
- Authorisation required: Casting Assistant/Casting Director/Executive Producer
- Returns: 

```json5
{
    "movie": [
        {
            "id": 14,
            "release_date": "Sat, 02 Feb 3202 00:00:00 GMT",
            "title": "Dark Night"
        },
        {
            "id": 14,
            "release_date": "Sat, 02 Feb 3202 00:00:00 GMT",
            "title": "Dark Night"
        }
    ],
    "success": true
}
```

### GET '/movie/1'

- Fetches a dictionary of one movie
- Authorization required: Casting Assistant/Casting Director/Executive Producer
- Returns: 

```json5
{
    "movie": [
        {
            "id": 14,
            "release_date": "Sat, 02 Feb 3202 00:00:00 GMT",
            "title": "Dark Night"
        }
    ],
    "success": true
}
```

### DELETE '/movie/1'

- Deletes a movies
- Authorization required: Executive Producer
- Returns: 

```json5
{
    "deleted": 2,
    "success": true
}
```
### PATCH '/movies/1'

- Update movies title
- Authorization required: Casting Director
- Request Arguments: Movies body
 

```json
{
    "title": "Mad Max",
    "release_date": "5-6-2020"
}
```
- Returns: 

```json5
{
    "movie": [
        {
            "id": 14,
            "release_date": "Sat, 02 Feb 3202 00:00:00 GMT",
            "title": "Dark Night"
        }
    ],
    "success": true
}
```




## Errors

### Bad request (400)

```json5
{
  'success': false,
  'error': 400,
  'message': 'Bad request'
}
```

### Not found  (404)

```json5
{
  'success': false,
  'error': 404,
  'message': 'Resource Not Found'
}
```

### Unprocessable request (422)

```json5
{
  'success': false,
  'error': 422,
  'message': 'Unable to process request'
}
```
### Duplicate (409)

```json5
{
  'success': false,
  'error': 409,
  'message': 'Duplicate found'
}

### Internal server error (500)

```json5
{
  'success': false,
  'error': 500,
  'message': 'Internal server error'
}
```

https://moviecast.auth0.com/authorize?audience=moviecast&
  response_type=token&
  client_id=Q4o4NhFT3MxMWfgFLIv5T0ZS0L5pMJD1&
  redirect_uri=http://localhost:8080