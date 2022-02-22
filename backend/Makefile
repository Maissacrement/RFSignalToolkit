#!make

DOCKER:=@docker
APP_NAME=radio
VERSION=1.0.9
REGISTRY=registry.gitlab.com/maissacrement/radio

env:=.env
include $(env)

login:
	${DOCKER} login registry.gitlab.com

app:
	python3 app.py &>/dev/null &
	tail -f ./debug.json

build:
	${DOCKER} build -t ${APP_NAME} .

start:
	${DOCKER} run --env-file ${env} -p ${PORT}:${PORT} -d ${APP_NAME}

reload:
	${DOCKER} run --env-file ${env} -v ${PWD}:/app -p ${PORT}:${PORT} -it ${APP_NAME}

notebook: build
	docker run --env-file ${env} -v ${PWD}:/app -p 8888:8888 -it ${APP_NAME} --entrypoint jupyter notebook --allow-root

tag-latest:
	@echo 'create tag latest'
	@docker tag $(APP_NAME) $(REGISTRY):latest

tag-version:
	@echo 'create tag $(VERSION)'
	@docker tag $(APP_NAME) $(REGISTRY):$(VERSION)

git:
	@git add .
	@git commit -m "$${msg:-"Up to date"}"
	@git push

push: git login build tag-version tag-latest
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	@docker push $(REGISTRY):$(VERSION)
	@docker push $(REGISTRY):latest

${APP_NAME}: build start
${APP_NAME}_dev: build reload