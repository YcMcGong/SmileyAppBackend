# SmileyAppBackend
	Third version of SmileyAppBackend, completely migrated to AWS and microservices architecture.

## System Design
	The following is the diagram of the smileyBackend. It contains mciro-services and web applications.
![alt text](https://drive.google.com/open?id=1nHWYZ8eu_TAPfSvVobs4iM4icbiAxN8n)

## Flask Skeleton
	This repo provides a flask web service skeleton with a ready to deply nginx container under the /flaskSkeleton folder.
	Suggests running micro-services using this skeleton.

#### Add python package

	To add python package, add the package name into /app/requirements.txt

#### Run as local server
* `python main.py`


## Django Skeleton
	This repo provides a Django web service skeleton with a ready to deply nginx container under the /djangoSkeleton folder.
	Suggest to use this skeletion while developing front-end internet facing web services.

#### Add python package

	To add python package, add the package name into /app/requirements.txt

#### Before running local server

	Need to perform a data migration first as following.
 
* `python3 manage.py makemigrations`
* `python3 manage.py migrate --run-syncd`

#### Run as local server
* `python manager.py runserver`


## Production using container

#### Build image

	This step requires sudo. Suggest sign in as super user using 'su'.

	Build image:
	
* `docker build -t <image_name> .`

#### Run image

* `docker run --rm -d -p 4000:80 <image_name>`

		Note:
			 - d: detach (run contianer in the background)
			 - p: map outside port: insider port
			--rm: remove the container upon exit

#### Push to docker for deployment

##### 1. Tag the image

* `docker tag SOURCE_IMAGE[:TAG] account/repository:tag`
	Current default format for this project: 
* `docker tag SOURCE_IMAGE[:TAG] mcgong/service_name:version`

##### 2. Login using docker credentials
	* `docker login`

##### 3. Push to docker
* `docker push account/repository:tag`
	Current default format for this project: 
* `docker push mcgong/service_name:version`

##### 4. Notify the maintainer through slack
	Notify the maintainer at the SmileyApp backend team on Slack.
	Need to mention: 
		1. service_name
		2. version
		3. commit message

#### Debug

	Bash into container to check files
* `docker run -ti -p 4000:80 <image_name> bash`


## License

### All Rights Reserved
	/* Copyright (C) Yicong Gong
	Authorized contributors granted copy rights for this software.
	All rights reserved, for demostration and collaboration purpose only.

### External open-source license
	There are a few open-source codes in this project from other authors.

#### Nginx-flask docker file
	The nginx-flask docker file itself is under Apache license from other author.
	Its original repo is here:

	https://github.com/tiangolo/uwsgi-nginx-flask-docker

#### Nginx-django docker file

	Derivatived work based on the following author. 
	The orginal License is attachd below:

	Copyright 2013 Thatcher Peskens
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

    	http://www.apache.org/licenses/LICENSE-2.0

	 Unless required by applicable law or agreed to in writing, software
	 distributed under the License is distributed on an "AS IS" BASIS,
	 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	 See the License for the specific language governing permissions and
	 limitations under the License.

