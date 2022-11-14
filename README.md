# Casting Agency

## Getting Started

### Introduction

#### Motivation

The Udacity Casting Agency Project is developed to cater to the needs of the casting agency to catalog and manage movies and actors details in a cantral manner with a web application for increased availability. Role Based Access Control is Implemented in teh application to maintain the data integrity and security.

#### URL
This applicaiton is hosteed in Heroku and is available in the following url.
The application requires authentication with email id and password and a role assigned to the user.
A postman collection is also attached to test the application
`https://castingagency9559.herokuapp.com/`

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the application root directory `./` first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=src/api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### API Specification

The following are the endpoints configured for the Casting Agency Application.
In addition to the parameters given in the below API spec, Auth Bearer token 
`headers={"Authorization": "Bearer " + <token>}  `
has to be added in each API call for the user to be authorised based on the role assigned.

`GET /movies`

- This endpoint returns the information about all the movies in the database.
- Request Arguments: None
- Sample Request
  ```
  curl -X get http://localhost:5000/movies
  ```
- Sample Response
```json
{
    "movies": [
        {
            "genre": "Thriller",
            "id": 1,
            "releasedate": "Wed, 11 Nov 2020 00:00:00 GMT",
            "title": "Gameover"
        },
        .
        .
        .
        {
            "genre": "fiction",
            "id": 6,
            "releasedate": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "ABC"
        }
    ],
    "success": true,
    "total_movies": 5
} 
```

`GET /movies/<id>`

- This endpoint returns the information about moviefor which id is given, from the database.
- Request Arguments: id
- Sample Request
  ```
  curl -X get http://localhost:5000/movies/1
  ```
- Sample Response
```json
{
    "movie": 
        {
            "genre": "fiction",
            "id": 1,
            "releasedate": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "ABC"
        },
    "success": true
}
```

`POST '/movies'`

- To post a new movie to the database
- Request Arguments:
  - `title`: The movie title to be added. String.
  - `releasedate`: The release date of movie to be added. Date.
  - `genre`: The genre of movie to be added. Integer.
- Returns: An object with keys, 
  - `created`, that contains the id of the created movie
  - `questions`, List of movies from the database
  - `success`, set to true
  - `total_movies`, that contains the count of movies currently in the database.
- Sample request: 
```  
curl -X POST http://localhost:5000/movies -H "Content-type: application/json" -d "{\"title\":\"ABC\",\"releasedate\": \"2022-10-10\",\"genre\":\"drama\" }" 
```
- Sample response:
```json
{
    "created": 1,
    "movies": [
        {
            "genre": "drama",
            "id": 1,
            "releasedate": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "ABC"
        }
    ],
    "success": true,
    "total_movies": 1
}
```

`PATCH '/movies/<id>'`

- To post a new movie to the database
- Request Arguments:
  - `id`: The id of movie to be updated.
  - `title`: The movie title to be updated. String.
  - `releasedate`: The release date of movie to be updated. Date.
  - `genre`: The genre of movie to be updated. Integer.
- Returns: An object with keys, 
  - `updated`, that contains the id of the created movie
  - `movie`, Updated movie from the database
  - `success`, set to true
- Sample request: 
```  
curl -X PATCH http://localhost:5000/movies/1 -H "Content-type: application/json" -d "{\"genre\":\"fiction\" }" 
```
- Sample response:
```json
{
    "updated": 1,
    "movie": {
            "genre": "fiction",
            "id": 1,
            "releasedate": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "ABC"
        },
    "success": true
}
```

`DELETE /movies/<id>`

- This endpoint deletes the movie with given id from the database.
- Request Arguments: id
- Sample Request
  ```
  curl -X DELETE http://localhost:5000/movies/1
  ```
- Sample Response
```json
{
    "total_movies": 0,
    "deleted":1,
    "success": true
}
```

`GET /actors`

- This endpoint returns the information about all the actors in the database.
- Request Arguments: None
- Sample Request
  ```
  curl -X get http://localhost:5000/actors
  ```
- Sample Response
```json
{
    "movies": [
        {
            "age": 43,
            "gender": "M",
            "id": 1,
            "name": "Tom Cruise"
        },
        .
        .
        .
        {
            "age": 45,
            "gender": "M",
            "id": 5,
            "name": "Vin Diesel"
        },
    ],
    "success": true,
    "total_movies": 5
} 
```

`GET /actors/<id>`

- This endpoint returns the information about actor with given id from the database.
- Request Arguments: id
- Sample Request
  ```
  curl -X get http://localhost:5000/actors/1
  ```
- Sample Response
```json
{
    "actor": 
        {
            "age": 43,
            "gender": "M",
            "id": 1,
            "name": "Tom Cruise"
        },
    "success": true
}
```

`POST '/actors'`

- To post a new actor detail to the database
- Request Arguments:
  - `name`: The name of actor to be added. String.
  - `age`: The age of actor to be added. Date.
  - `gender`: The gender of actor to be added. Integer.
- Returns: An object with keys, 
  - `created`, that contains the id of the created actor
  - `actors`, List of actors from the database
  - `success`, set to true
  - `total_actors`, that contains the count of actors currently in the database.
- Sample request: 
```  
curl -X POST http://localhost:5000/actors -H "Content-type: application/json" -d "{\"name\":\"Tom Cruise\",\"age\": \"43\",\"gender\":\"M\" }" 
```
- Sample response:
```json
{
    "actors": [
        {
            "age": 43,
            "gender": "M",
            "id": 1,
            "name": "Tom Cruise"
        }
    ],
    "created": 1,
    "success": true,
    "total_actors": 1
}
```

`PATCH '/actors/<id>'`

- To update an actor in the database
- Request Arguments:
  - `id`: The id of movie to be updated.
  - `name`: The name of actor to be updated. String.
  - `age`: The age of actor to be updated. Date.
  - `gender`: The gender of actor to be updated. Integer.
- Returns: An object with keys, 
  - `updated`, that contains the id of the updated actor
  - `movie`, Updated actor from the database
  - `success`, set to true
- Sample request: 
```  
curl -X PATCH http://localhost:5000/actors/1 -H "Content-type: application/json" -d "{\"age\":53 }" 
```
- Sample response:
```json
{
    "updated": 1,
    "actor": {
            "age": 53,
            "gender": "M",
            "id": 1,
            "name": "Tom Cruise"
        },
    "success": true
}
```

`DELETE /actors/<id>`

- This endpoint deletes the actor detail with given id from the database.
- Request Arguments: id
- Sample Request
  ```
  curl -X DELETE http://localhost:5000/actors/1
  ```
- Sample Response
```json
{
    "total_actors": 0,
    "deleted":1,
    "success": true
}
```


### Setting up Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new web application
4. Create a new API `moviecast`
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`
   - `get:actors`
   - `post:actors`
   - `patch:actors`
   - `delete:actors`

6. Create new roles for:
   - Casting Assistant
     - can `get:movies`
     - can `get:actors`

   - Casting Director
     - All permissions a Casting Assistant has and
     - can `patch:movies`
     - can `post:actors`
     - can `patch:actors`
     - can `delete:actors` 

   - Executive Producer
      - Has all permissions

7. Test the endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant, Casting Director and Executive Producer role.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for each roole, navigate to the authorization tab, and including the respective JWT in the token field.
   - Run the collection.


