.PHONY: deploy

deploy:
	cd deploy && ./deploy.sh

delete:
	cd deploy && ./delete.sh

test:
	cd lambda && pytest
