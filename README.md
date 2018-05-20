# SmileyAppBackend
	Third version of SmileyAppBackend, completely migrated to AWS and microservices architecture.
#### MySmileApp Project
![alt text](https://s3-us-west-1.amazonaws.com/smileyfilehostpublic/mysmile_100.jpg)
	
	MySmileApp is a collabration project for programmers who love urban-exploration to:
	
	1. Test and try out their new programming ideas.
	2. Build a group of cloud-based micro-services to find interesting places to go for the weekend.
	
#### Table of content
	1. System Design
	2. Flask Skeleton
	3. Django Skeleton
	4. Docker container for deployment
	5. Endpoints
	6. AWS credentials
	7. License

## 1. System Design
	The following is the diagram of the smileyBackend. It contains mciro-services and web applications.
![alt text](https://s3-us-west-1.amazonaws.com/smileyfilehostpublic/design_3.png)
#### a) Web Server
	A Django based internet facing server to process the requests from the mobile/web front end.
#### b) AuthService
	Authenticate user credential, hanlde sign up, and store user data
#### c) attractionService
	Manage attraction, and automatically attach post for the same attraction into the news feed of the corresponding attraction.
#### d) relationService
	Manage user-user, user-attraction relations. It is basically a graph database built on top of DynamoDB. attractionService will notify relationService for any new post. relationService will publish these changes to the mapService.
#### e) mapService
	It renders a list of attractions for each user.

## 2. Flask Skeleton
	This repo provides a flask web service skeleton with a ready to deply nginx container under the /flaskSkeleton folder.
	Suggests running micro-services using this skeleton.

#### Add python package

	To add python package, add the package name into /app/requirements.txt

#### Run as local server
* `python main.py`


## 3. Django Skeleton
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

## 4. Docker container for deployment

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

## 5. Endpoints

#### a) Test endpoint
	webServer: localhost:3000
	authService: localhost:4000
	attractionService: localhost:6000
	relationService: localhost:7000
	mapService: localhost:8000

#### b) Production endpoint
	Production endpoint will be managed by route 53 and load balancer.
	webServer: web.mysmileapp.com
	authService: auth.mysmileapp.com
	attractionService: attraction.mysmileapp.com
	relationService: relation.mysmileapp.com
	mapService: map.mysmileapp.com

## 6. AWS credentials
	For testing, all credential should be placed into a file named config.py.
	The name config.py is added into the .gitignore file, and will be ignored when pushing to github.
	In production, all EC2 instances will be assign IAM roles, there is no need to attach credentials into the code.

## 7. License

### All Rights Reserved
	/* Copyright (C) 2018 Yicong Gong & Repo Collabrators
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

