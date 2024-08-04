# weather-forecast

## Overview

This Django application provides two APIs which are:
1. Get a list of 10 coolest district from current date to 7 days in Bangladesh.
2. Compare the temperature at 2 PM on a specific date between a user's location and their travel destination to provide travel advice.

## Setup

### Clone the Repository

Clone the repository using:

```bash
$ git clone https://github.com/zxalif/weather-forecast.git
```
Go to the project directory: 
```bash
$ cd weather-forecast
```
Create a virtual environment and activate it, after activating it install the dependency. Run this command one by one to migrate the project, the project is running on default django db. 
```bash
# virtual env
$ python -m venv venv
# activate 
$ source venv/bin/activate
# install dependency
$ pip install -r requirements.txt
# create the migrations
$ python manage.py makemigrations
# migrate to db 
$ python manage.py migrate
```

# Run the server
```bash
python manage.py runserver
```

There is two command specificly use this project, one is for getting the list of district from github and another is going to be a crontab use for updating the weather data, 
```bash
# its going to load all the district into the db
$ ./manage.py load_districts
# its going to collect the next 7 days wether from today.
$ ./manage.py update_weather_data
```

# Now lets set up the cron tab
we are going to set it for every day, you can set it as your liking. 
```bash
# this will open an editor, add the bellow line at the end of the file
# use `sudo` if required
$ crontab -e 
0 0 * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py update_weather_data
```

# API
## COOLEST DISTRICT
```bash
$ curl -X GET http://localhost:8000/api/v1/weather/coolest-district/

# you will get a response like this
[
    {
        "name": "Cox's Bazar",
        "avg_temp": 29.042857142857144
    },
    ....
]
```
## TRAVEL ADVICE
```bash
$ curl -X GET http://localhost:8000/api/v1/weather/trave-advice/64/1/2024-08-08/

# you will get a response like this
{
    "from": "Satkhira",
    "from_temp": 29.9,
    "destination": "Dhaka",
    "destination_temp": 29.9,
    "advice": "Same temperature, wouldn't hurt to travel!"
}
```

FEEL FREE TO RAISE A BUG
