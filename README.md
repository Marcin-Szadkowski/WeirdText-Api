Weird Text API
==============
See app at Heroku [App docs](https://weird-api.herokuapp.com/docs#)

Usage
-----
This is project to handle encoding of weird text and decoding. It exposes two endpoints:
  1. POST /v1/encode/
  1. POST /v1/decode/ 
  
  with json payload
  ```
  {
    "text": "your text"
  }
  ```
  
  Development
  -----------
  
  ### Requirements
  
    - docker
    - python>=3.8
    
  To run project locally go to */backend* directory and type:
  ```
  docker-compose up --build
  ```
  Then your local server is available at (http://localhost:8080)
  
  Tests
  -----
  To run tests inside docker container run
  ```
  docker-compose exec api pytest
  ```
  
  Deploy
  ------
  Manual deploy script is located in tools/release.sh
 
  To deploy automatically using configured *heroku.yml*
  ```
  git push heroku master
  ```
  
  
