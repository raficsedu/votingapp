# Employer voting app to chose restaurant

Company needs internal service for its’ employees which helps them to make a decision on lunch place. Each restaurant will be uploading menus using the system every day over API and employees will vote for the menu before leaving for lunch.


## Install
First clone this project into your machine/pc. This project can be run into both **Docker** and **Virtual Environment**

### Docker
1. Clone the project with ..
    ```
    git clone https://github.com/raficsedu/votingapp.git
    ```
2. Install ***Docker*** and ***Dcoker Composer*** from their official web site based on your machine OS.
3. Create a .env file in the directory where the settings.py file resides and chage the database name, user and pass according to your choice.

    ```
    SECRET_KEY=django-insecure-pku+v1sfow-d#p)--e^8cgti2-csfb_6x-&idobcpc2a8pvql9
    DEBUG=True
    POSTGRES_HOST_NAME=db
    POSTGRES_NAME=voting_app  
    POSTGRES_USER=postgres  
    POSTGRES_PASSWORD=@mypass
    ```
    Use the same POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD value in docker-compose.yml file in db service under environment section.
    ```
    environment:  
      - POSTGRES_USER=postgres  
      - POSTGRES_PASSWORD=@mypass  
      - POSTGRES_DB=voting_app
    ```
4. Go to the project directory and run ..
    ```
    1. sudo docker-compose build
    2. sudo docker-compose up
    ```
5. Migrate all the migration files ..
    ```
    sudo docker-compose run web python manage.py migrate
    ```
 
6. If the build throws error due to log folder missing, then you need to create a folder named "log" in the project root directory.

Now open up your browser and navigate to http://127.0.0.1:8000.


### Virtual Environment
1. Clone the project with ..
	```
	git clone https://github.com/raficsedu/votingapp.git
	```
2. Install ***Virtual Environment*** using pip.
3. Create a .env file in the directory where the settings.py file resides and chage the database name, user and pass according to your choice. Create the database in your machine Postgresql.

	```
	SECRET_KEY=django-insecure-pku+v1sfow-d#p)--e^8cgti2-csfb_6x-&idobcpc2a8pvql9
	DEBUG=True
	POSTGRES_HOST_NAME=127.0.0.1
	POSTGRES_NAME=voting_app  
	POSTGRES_USER=postgres  
	POSTGRES_PASSWORD=@mypass
	```
4. Go to the project directory and run ..
	```
	1. source env/bin/activate
	2. pip install -r requirements.txt
	3. python manage.py migrate
	4. python manage.py runserver
	```

Now open up your browser and navigate to http://127.0.0.1:8000.

## Error log and Automatic Test

All exceptions and logs will be written into error.log file. So create a folder named "log" into your main project root directory and error.log file will create automatically.
```
log/error.log
```
For running all the automatic test cases, run the following commands. You must need to be inside virtual environment or into docker container.
```
1. python manage.py test employer
2. python manage.py test restaurant
3. python manage.py test common
4. python manage.py test vote
```

## API Documentation

You can rename the current file by clicking the file name in the navigation bar or by clicking the **Rename** button in the file explorer.

### Employer
1. Create employer
	```
	POST /api/employer/list HTTP/1.1
	Host: 127.0.0.1:8000
	Content-Type: application/json
	Content-Length: 185

	{
	    "first_name": "Muntasir",
	    "last_name": "Rahman",
	    "email": "employer@myapp.com",
	    "password": "@CYLINRAf45",
	    "age": 33,
	    "gender": 1,
	    "phone": "01719454466"
	}
	```
	Response be like
	```
	{
	    "id": 7,
	    "first_name": "Muntasir",
	    "last_name": "Rahman",
	    "username": "employer",
	    "email": "employer@myapp.com",
	    "age": 33,
	    "gender": 1,
	    "phone": "01719454466",
	    "created_at": "2021-12-27T08:58:12.601592Z"
	}
	```
### Restaurant
1. Create restaurant
	```
	POST /api/restaurant/list HTTP/1.1
	Host: 127.0.0.1:8000
	Content-Type: application/json
	Content-Length: 179

	{
	    "name": "Restaurant 3",
	    "email": "restaurant@myapp.com",
	    "password": "@CYLINRAf45",
	    "address": "House x/y Road 0z Kallyanpur Dhaka",
	    "phone": "01719454466"
	}
	```
	Response be like
	```
	{
	    "id": 5,
	    "username": "restaurant",
	    "email": "restaurant@myapp.com",
	    "name": "Restaurant 3",
	    "address": "House x/y Road 0z Kallyanpur Dhaka",
	    "phone": "01719454466",
	    "created_at": "2021-12-27T09:04:07.504046Z"
	}
	```
2. Create menu
	```
	POST /api/restaurant/menu/list HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 2b10039454256dbdafbf5b803f1bc8573a504db8
	Content-Type: application/json
	Content-Length: 263

	{
	    "date": "",
	    "menus": [
	        {
	            "item": "Polao",
	            "price": 200
	        },
	        {
	            "item": "Roast",
	            "price": 150
	        },
	        {
	            "item": "Beef",
	            "price": 180
	        }
	    ]
	}
	```
	Response be like
	```
	{
	    "date": "",
	    "menus": [
	        {
	            "item": "Polao",
	            "price": 200
	        },
	        {
	            "item": "Roast",
	            "price": 150
	        },
	        {
	            "item": "Beef",
	            "price": 180
	        }
	    ]
	}
	```
3. Get menu
	```
	GET /api/restaurant/menu/list HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token ae801cd01245ff4951cd3ec62d9a574546724834
	```
	Response be like
	```
	[
	    {
	        "restaurant_id": 5,
	        "date": "2021-12-27",
	        "menus": [
	            {
	                "item": "Polao",
	                "price": 200.0
	            },
	            {
	                "item": "Roast",
	                "price": 150.0
	            },
	            {
	                "item": "Beef",
	                "price": 180.0
	            }
	        ]
	    },
	    {
	        "restaurant_id": 6,
	        "date": "2021-12-27",
	        "menus": [
	            {
	                "item": "Polao",
	                "price": 200.0
	            },
	            {
	                "item": "Roast",
	                "price": 150.0
	            },
	            {
	                "item": "Beef",
	                "price": 180.0
	            }
	        ]
	    }
	]
	```
### Employer/Restaurant Authentication
1. Authentication body is same for employer and restaurant.
	```
	POST /api/authenticate HTTP/1.1
	Host: 127.0.0.1:8000
	Content-Type: application/json
	Content-Length: 68

	{
	    "email": "employer@myapp.com",
	    "password": "@CYLINRAf45"
	}
	```
	Response be like
	```
	{
	    "id": 12,
	    "first_name": "Muntasir",
	    "last_name": "Rahman",
	    "username": "employer",
	    "email": "employer@myapp.com",
	    "employer_id": 7,
	    "age": 33,
	    "gender": 1,
	    "phone": "01719454466",
	    "token": "ae801cd01245ff4951cd3ec62d9a574546724834"
	}
	```
2. Logout body is same for employer and restaurant.
	```
	GET /api/logout HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token f9400b53d8a408b57b9f97bb0934c8da396add0e
	```
	Response be like
	```
	{
	    "message": "Successfully logged out"
	}
	```
### Vote
1. Create vote
	```
	POST /api/vote/list HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 37c4b9e24a5c98c1f078f2c143ccc0b82cff8d82
	Content-Type: application/json
	Content-Length: 38

	{
	    "restaurant": 2,
	    "vote": 1
	}
	```
	Response be like
	```
	{
	    "id": 1,
	    "restaurant": 2,
	    "vote": 1,
	    "created_at": "2021-12-27T09:44:24.068864Z"
	}
	```
2. Vote result
	```
	POST /api/vote/result HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token f9400b53d8a408b57b9f97bb0934c8da396add0e
	Content-Type: application/json
	Content-Length: 18

	{
	    "date": ""
	}
	```
	Response be like
	```
	{
	    "restaurant_id": 2,
	    "restaurant__name": "Restaurant 3",
	    "votes": 1
	}
	```

## All the available API's
```
1. http://127.0.0.1:8000/api/employer/list
2. http://127.0.0.1:8000/api/restaurant/list
3. http://127.0.0.1:8000/api/restaurant/menu/list
4. http://127.0.0.1:8000/api/authenticate
5. http://127.0.0.1:8000/api/logout
6. http://127.0.0.1:8000/api/vote/list
7. http://127.0.0.1:8000/api/vote/result
```