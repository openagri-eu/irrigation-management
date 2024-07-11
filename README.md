# irrigation-management
The Irrigation management service provides a toolkit of irrigation related tools. 

# Dependencies
This service depends on docker[27.0.3] and python[3.11]

# Running
To run this service, first navigate to the root folder via terminal, and run:\
docker build -t irrigation .\
Then, once it builds the image, run:\
docker run -d --name irrigation -p 80:80 irrigation\

Then, you'll be able to access the backend via localhost/docs.
