# leaderboard
Distributed leaderboard using Redis Enterprise Actve-Active

## Running application as a Python code

First set the env variables like host, port, password and location:

    export HOST=redis-19781.c1.us-east1-2.gce.cloud.redislabs.com
    export PORT=19781
    export LOCATION=Mumbai
    export PASSWORD=eq71pQ1ewHOdLu1lBFL3haNEEWUvU3j8

Finally, execute this:    

    git clone https://github.com/Redislabs-Solution-Architects/leaderboard.git
    cd leaderboard
    pip install -r requirements.txt

## Running application behind GCP LB (Active-Active)

* Create separate instance templates for 2 regions (for Ubuntu 20.x): For instance: Beijing & Singapore OR Mumbai & Delhi
  Use following docker image: abhishekcoder/sample-leaderboard-app:latest
  The docker command to be used here: 
  sudo docker run -p 80:5555 -e HOST=<HOST_URL_REGION1> -e PORT=<PORT_REGION1> -e PASSWORD=<PASSWORD_REGION1> -e LOCATION=<REGION1> abhishekcoder/sample-leaderboard-app:latest

* Create respective instance groups for each of these instance templates (Beijing and Singapore)
* Create Global LB (HTTP), required backend service and associate this backend service with above created instance-groups. Include both Beijing and Singapore instance groups
* Goto browser and enter the LB IP address
