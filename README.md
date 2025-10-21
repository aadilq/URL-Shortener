# URL-Shortener

Currently in Production of building a URL-Shortener using Python,FastAPI, React, Docker, Redis, and PostgreSQL.

## Status Update 1

Right now, I have just set up the two basic API endpoints using FastAPI for:

-  /api/shorten_url: Takes in a normal Http URL and shortens it using a randomly generated six character short code. 
   -  For example, take "https://www.google.com/" 
   -  Using our function generate_short_code, we create a six character code. We store that six character code in our database and map it to the original url. Right now we are just using a dictionary as a makeshift database, we will sync it up with postgreSQL later. 
   -  We return the user the unique six character code, the original url, and the shortened url with the six digit code
 
   
 <img width="1265" height="500" alt="Screenshot 2025-10-03 at 12 42 33 PM" src="https://github.com/user-attachments/assets/5dc37abf-1a3a-4919-990a-ec175f95887f" />

   


-  /{short_code}: Takes in the unique six character code and returns to the user the original URL
   -  For example, in the screenshot below, our unique six character code is "dnIgbT". We take the code and search in our dictionary. If it is not found in the dictionary, we raise an HTTPException error, else we retrieve the original url
 
<img width="1278" height="494" alt="Screenshot 2025-10-03 at 12 42 43 PM" src="https://github.com/user-attachments/assets/cb1ace10-b837-499f-8bfc-c7ccb962a185" />


## Status Update 2
For the second part of the project, I am working on implementing a PostGRES database as the primary database for the URL-Shortener. The first step in creating our url-shortener database was making the database within postgres and it started off by making sure that I already had postGRES installed on my machine, which I confirmed when running 'psql --version'. I then connected into the postgres system as the postgres superuser. The last step was creating the database 'url_shortener' with the dedicated user 'url-user'. 



## Status Update 3 
After creating the 'url_shortener' database, it was time to connect it to our main url-shortener application. The first step was creating the connection string with our database credentials and adding it our dotenv file. With the help of GenAI tools such as Claude, I was able to load the database environmental variable from our dotenv file and store it as a variable. 

-  Next up, I also used Claude as a guiding tool to help me connect the our database to the main application. I had to create a database engine which establishes connectivity to our PostgreSQL database engine. This function returns an engine instance which acts as the central communication of our database. 

`database_engine = create_engine(DATABASE_URL)`



- After establishing connectivity from our application to the postgresSQL database, Claude recommended to create a sessionLocal class which is a factory for creating database sessions. Each instance is a database session

`Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)`


## Status Update 4

Defined the table structure of our `url-shortener` database in the `models.py` file. Before talking about the `models.py` file, let's go back to the `database.py` where we had written a line of code which was essential for creating our table and it was...


`Base = declarative_base()`

- This line of code allows us to use the declarative style in order to define our database models as Python classes, which is really convenient. 

In `models.py`, we defined the structure of our `url-shortener` table in which the columns are as define: 


`id` -> Primary key which will auto increment e.g.(1, 2, 3,...)

`short_code` -> The shortened code e.g.(dnIqbT)

`original_url` -> The original url that we're shortening 

`created_at` -> automatic timestamp when the shortened url was created

`click_count` -> Tracks how many times the short url has been clicked

## Status Update 5
Replace our in-memory database of a python dictionary with the postgreSQL database. In the `shorten_url` function of our POST request, with the help of Claude, I added a dependency injection that FastAPI offers which calls the `get_db()`, gets a database session and passes it to the function to the db parameter. Once the function finishes, the session is closed. 

`db: Session = Depends(get_db)`


We then query our database for records from the URL model to make sure if our short code is unique. 


`    while(db.query(models.URL).filter(models.URL.short_code == short_code)).first():
         short_code = generate_short_code()`

let's break it down, 

- `db.query(models.URL)` -> query the url-shortener table in `models.py`. `models.URL` refers to the URL python class that we made in `models.py`, and this stores our url-shortener table. 

- .filter(models.URL.short_code == short_code) -> checks if the any of the short codes in our database matches the short code that we just generated. 

- .first() -> returns the first instance of the short code if it does appear in our database. 


After we check that our shorted code does not exist in our, we create a new object that comforms to the url model that we defined in `models.py` and save it to our database. 

`    db_url = models.URL(
        short_code = short_code, 
        original_url = str(request.url),
        click_count = 0
    )`


## Status Update 6 
I added another GET endpoint to the FastAPI backend in order to get the statistics for each shortened url for analytics. In this GET endpoint, we taken in the shortened code that we made for the URL, find it within our database, and return the short code, the original url, how many times this shortened_url has been clicked, and what date/time that the shortened url was created at. I also tweaked the way in which I was accessing my database. Instead of relying on FastAPI dependency injection, I changed it up and went with the manual way of creating a database session using try and finally blocks. 


## Status Update 7 
I transitioned into the frontend of my application, focusing on what the user is going to see. First, we had to resolve CORS issue since our frontend and backend were running on two different ports. In my main.py file, I allowed cors access to the the port in which the frontend react is living in so that the data can be transferred back and forth. I then worked on building the UrlShortener.jsx component for our application, which consists of a function called handlesubmit in order use our POST request and create the shortened url in our FastAPI backend. 

## Status Update 8
Worked on using Docker to containerize our application. First, I had to create two separate Docker files for both the backend and frontend of the url shortener, which I then had claude help me out on what commands are needed to create our images. Now I am going to work on building out `docker-compose.yml` at the root of our project. 

## Status Update 9
Finished on dockerizing the url-shortener. I've never worked with docker all at before this project so I leveraged Claude in order to explain how I could dockerize the url-shortener so that it could be run on other machines without the need to download anything. The first step was downloading docker desktop on my laptop which I proceeded to do from the offial [docker website](https://www.docker.com/). Claude then instructed me to first containerize the backend part of the url-shortener which involved first creating a Dockerfile. Within the Dockerfile, we essentially give it a "recipe" for a container that has everything the backend needs including the version of python we needed, all of our code, and the dependencies that we installed. We then built an image of our backend by running `docker build -t url-shortener-backend .` The same steps applied to the frontend but with different commands. We then Orchestrated Everything with a `docker-compose.yml` file at the root file of our project which we defined how our three containers are working together. Last but not least, I ran `docker-compose up` which built our three images(postgres, backend, frontend), created a Docker Network in which all of our three containers can talk to each other and is separated from other docker projects. 

# Status Update 10
Got around to start implementing Redis as a caching service in our url-shortener. Right now the way that our application works is that our user clicks on the short url, which then allows our backend to query postgresql, gets the original url, and redirects the user. Now, with the Redis implemented, the user clicks on the short url, checks our Redis Cache and if its not cached yet, query postgresql, and then Store in the Redis cache for 24 hours. Now when the user clicks on the same link within the next 24 hours, the link will be pulled from our Redis cache. 


## Status Update 11
Finished implementing the Redis caching in our url-shortener. The first part of the implementation actually dealt with the Docker aspect of it which meant adding it our `requirements.txt` file so that it could be read in our backend container. Then we added it to our docker-compose.yml file as its own service. We also made a tweak to our backend container and added redis as a dependency because technically our backend relies on redis to recieve data. Next up was creating our redis_client.py file in which we defined two functions, `get_cached_url` and `cache_url`, both of which deal directly with retrieving the original link from the cache and adding it to the cache if it was not already there. 