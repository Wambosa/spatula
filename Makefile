.PHONY: info install lint test build deploy shim run prepare_zip prepare_zip_container find_distinct_concept terraform clean python_package_manager

PROJECT            := spatula
PREFIX             := spat
EXT                := py
TF_VER             := 0.12.12
BUILD_LOCAL_DIR    := .build

# 
# Common Repositry Activities
# 
info:
	@pipenv graph \
	&& pipenv run python --version

install:
	@make -s python_package_manager \
	&& mkdir -p ${BUILD_LOCAL_DIR} \
	&& make -s clean \
	&& pipenv install --dev \
	&& pipenv run python --version

install_apple:
	@brew install pyenv \
	&& brew install pipenv \
	&& mkdir -p ${BUILD_LOCAL_DIR} \
	&& make -s clean \
	&& pipenv install --dev --skip-lock \
	&& pipenv run python --version

lint:
	@make --no-print-directory prepare_zip_container \
	&& pipenv run pylint --rcfile=config/pylintrc ./${BUILD_LOCAL_DIR}/**/*.py

test:
	@pipenv run pytest --disable-pytest-warnings -vv

# 
# Local development
# 

# standup some fake resources to target for isolated realtime integration testing
shim:
	@docker-compose -f ./tests/docker-compose.yml up --build

# execute a function with whatever parameters required
# this is an alternate and faster method, vs refreshing a docker container
run:
	@make -s --no-print-directory prepare_zip_container \
	&& cd ${BUILD_LOCAL_DIR}/${FUNC} \
	&& echo RUNNING: ${FUNC}.${EXT} \
	&& pipenv run python main.${EXT} $(RUN_ARGS)

# 
# Helpers
# reused multiple times by other actions

prepare_zip:
	@rm -rf ${BUILD_DIR}/${NAME} \
	&& mkdir -p ${BUILD_DIR}/${NAME}/lib \
	&& pipenv lock -r > ${BUILD_DIR}/${NAME}/requirements.txt \
	&& cp ./src/common/${WRAPPER} ${BUILD_DIR}/${NAME}/main.${EXT} \
	&& cp ./src/common/context.${EXT} ${BUILD_DIR}/${NAME}/context.${EXT} \
	&& cp ./src/lib/* ${BUILD_DIR}/${NAME}/lib/ \
	&& cp ./src/func/${NAME}.${EXT} ${BUILD_DIR}/${NAME}/func.${EXT} \
	&& test -f ./config/${NAME}.yml && cp ./config/${NAME}.yml ${BUILD_DIR}/${NAME}/const.yml || echo ;\

prepare_zip_container:
	@CONTAINERS="scrape" \
	&& echo "zipping detected containers: $$CONTAINERS" ;\
	for name in $$CONTAINERS ; do \
		make -s prepare_zip NAME=$$name WRAPPER=local_wrapper.${EXT} BUILD_DIR=${BUILD_LOCAL_DIR} ;\
	done

clean:
	@find ${BUILD_LOCAL_DIR}/ \! -name 'terraform' -delete ;\
	find . -name '__pycache__' -exec rm -rf "{}" \; > /dev/null 2>&1 ;

python_package_manager:
	@echo "installing pipenv"
	curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | sudo python
