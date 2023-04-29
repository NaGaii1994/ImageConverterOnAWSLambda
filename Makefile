.PHONY: deploy
.PHONY: frontend

frontend_build_on_devcontainer:
	yarn build

frontend_build_on_host:
	docker-compose -f docker-compose.dev.yml exec --user vscode lambda bash -c "cd /workspace && yarn && yarn build"

deploy_local: frontend_build_on_devcontainer
	cd deploy && ./deploy.sh local

deploy_ci: frontend_build_on_devcontainer
	cd deploy && ./deploy.sh ci

deploy_prod: frontend_build_on_host
	cd deploy && ./deploy.sh prod

e2e_test_local:
	python ./deploy/e2e_test.py

delete:
	cd deploy && ./delete.sh

test:
	cd lambda && pytest
