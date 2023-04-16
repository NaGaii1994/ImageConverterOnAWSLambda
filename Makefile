.PHONY: deploy

deploy_local:
	cd deploy && ./deploy.sh local

deploy_ci:
	cd deploy && ./deploy.sh ci

deploy_prod:
	cd deploy && ./deploy.sh prod

delete:
	cd deploy && ./delete.sh

test:
	cd lambda && pytest
