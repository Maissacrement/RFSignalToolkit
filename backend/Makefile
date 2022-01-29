#!make

DOCKER:=@docker
APP_NAME=radio

env:=.env
include $(env)

login:
	${DOCKER} login

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

${APP_NAME}: build start
${APP_NAME}_dev: build reload