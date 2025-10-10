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

In `models.py`, we defined the structure of our `urls` table in which the columns are as define: 


`id` - Primary key which will auto increment e.g.(1, 2, 3,...)

`short_code` - The shortened code e.g.(dnIqbT)

`original_url` - The original url that we're shortening 

`created_at` - automatic timestamp when the shortened url was created

`click_count` - Tracks how many times the short url has been clicked

