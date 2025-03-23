# CliZod - Abstract Classifier

This repo contains the jupyter notebooks for running the experiment the study **Accelerating Disease Model Parameter Extraction: An LLM-based Ranking
Approach to Select Initial Studies For Literature Review Automation**. 
Please see notbooks directory.

If you would like to run the code please follow the instructions below. 

## Prerequisite
You will need to install [Docker](https://docs.docker.com/get-docker/) before running the commands below.
You will need an API key from Open AI. Place the API key in a .\\.env file with the following key. 
```
OPEN_AI_API_KEY="<PLACE KEY HERE>"
```

## Run
You will need to use the docker-compose command on the command prompt.

Note: the first time you run this it will try and download the libraries defined in requirements.txt and may take a while. 

```
docker-compose up -d
```

If you make changes to requirements.txt make sure to add the build flag
```
docker-compose up --build -d
```

Navigate to [http://127.0.0.1:8888/lab/](http://127.0.0.1:8888/lab/) in a browser to view the notebooks in interactive mode.


## Stop
```
docker-compose down
```



