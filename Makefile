.PHONY: deploy

deploy:
	cd deploy && ./deploy.sh

test:
	cd lambda && pytest
