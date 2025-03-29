

PHONY: build-test-image
build-test-image:
	docker pull python:3.12
	docker build -t db-delta-test -f Dockerfile.test .

PHONY: run-test-image
run-test-image: build-test-image
	docker run --rm db-delta-test
