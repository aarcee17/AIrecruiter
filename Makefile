build:
	docker build -t recapp .

dockerRun:
	docker run -it --rm -p 8000:8000 recapp

herokuBuild:
	docker build --platform linux/amd64 -t recapp .

herokuDeploy:
	- heroku git:remote -a rec-app
	- docker tag recapp registry.heroku.com/rec-app/web
	- docker push registry.heroku.com/rec-app/web
	- heroku container:release web --app rec-app


