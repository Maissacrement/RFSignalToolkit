#!make

DOCKER:=@docker
APP_NAME=radio

env:=.env
include $(env)

login:
	${DOCKER} login

build:
	${DOCKER} build -t ${APP_NAME} .

start:
	${DOCKER} run --env-file ${env} -p ${PORT}:${PORT} -it ${APP_NAME}

${APP_NAME}: login build start