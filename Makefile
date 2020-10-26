.PHONY: install lint test build deploy shim sanity_check run watch prepare_zip prepare_zip_lambda prepare_zip_container register_container prepare_zip_layer find_distinct_concept terraform clean circleci

PROJECT            := spatula
PREFIX             := spat
EXT                := py
TF_VER             := 0.12.12
BUILD_LOCAL_DIR    := .build
BUILD_LAMBDA_DIR   := ./infra/lambda/.build
BUILD_LAYER_DIR    := ./infra/layer/.build/layer/python/lib/python3.7/site-packages

# 
# Common Repositry Activities
# 

install:
	@make -s terraform \
	&& make -s python_package_manager \
	&& make -s clean \
	&& pipenv install --dev \
	&& pipenv run python --version

lint:
	@make --no-print-directory prepare_zip_container \
	&& pipenv run pylint --rcfile=config/pylintrc ./${BUILD_LOCAL_DIR}/**/*.py \
	&& ${BUILD_LOCAL_DIR}/terraform fmt -recursive \
	&& ${BUILD_LOCAL_DIR}/terraform validate

test:
	@pipenv run pytest --disable-pytest-warnings -vv

# 
# Local development
# 

# standup some fake resources to target for isolated realtime testing
# note: this particular version of the command will steal one console window
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
	@CONTAINERS="$(shell make -s find_distinct_concept CONCEPT_PATH=./src/func)" \
	&& echo "zipping detected containers: $$CONTAINERS" ;\
	for name in $$CONTAINERS ; do \
		make -s prepare_zip NAME=$$name WRAPPER=local_wrapper.${EXT} BUILD_DIR=${BUILD_LOCAL_DIR} ;\
	done

find_distinct_concept:
	@echo "$(shell ls -I "terraform" -I "__pycache__" -I "__init__.tf" -I "vars.tf" ${CONCEPT_PATH} -1 | sed -e 's/\..*$$//')"

terraform:
	@echo "installing terraform ${TF_VER}"
	wget https://releases.hashicorp.com/terraform/${TF_VER}/terraform_${TF_VER}_linux_amd64.zip > /dev/null 2>&1 \
	&& unzip ./terraform_${TF_VER}_linux_amd64.zip -d . \
	&& rm -f ./terraform_${TF_VER}_linux_amd64.zip \
	&& chmod +x ./terraform \
	&& mkdir -p ${BUILD_LOCAL_DIR} \
	&& mv ./terraform ${BUILD_LOCAL_DIR}/terraform

clean:
	@rm -rf ${BUILD_LAMBDA_DIR} ;\
	rm -rf ${BUILD_LAYER_DIR} ;\
	find ${BUILD_LOCAL_DIR}/* \! -name 'terraform' -delete ;\
	find . -name '__pycache__' -exec rm -rf "{}" \; > /dev/null 2>&1 ;

python_package_manager:
	@echo "installing pipenv"
	curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | sudo python
