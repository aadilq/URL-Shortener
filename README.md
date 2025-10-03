# URL-Shortener

Currently in Production of building a URL-Shortener using FastAPI, Docker, Redis, and PostgreSQL.

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

