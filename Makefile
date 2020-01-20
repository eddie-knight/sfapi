TAG		:= $$(git log -1 --pretty=%H)
IMG		:= ${NAME}:${TAG}
LATEST	:= ${NAME}:latest

build:
	@docker build -t ${IMG} -f ${DIR}/Dockerfile ${DIR}
	@docker tag ${IMG} ${LATEST}

push:
	@docker push ${IMG}
	@docker push ${LATEST}

login:
	@docker login -u ${USER} -p ${PASS}
