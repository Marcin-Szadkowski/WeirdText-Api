#!/bin/bash
cd ..

heroku container:push web --app weird-api   

heroku container:release web --app weird-api