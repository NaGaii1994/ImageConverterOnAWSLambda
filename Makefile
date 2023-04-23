.PHONY: deploy

deploy_local:
	cd deploy && ./deploy.sh local

deploy_ci:
	cd deploy && ./deploy.sh ci

deploy_prod:
	cd deploy && ./deploy.sh prod

e2e_test_local:
	python ./deploy/e2e_test.py

delete:
	cd deploy && ./delete.sh

test:
	cd lambda && pytest
