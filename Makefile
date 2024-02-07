RUN=docker run -it --rm -p 5000:5000
DEV_IMAGE=doepy
docker-images: 
	docker build -t $(DEV_IMAGE) -f docker/Dockerfile.doepy .


PYTEST=pytest -o cache_dir=/tmp --quiet -rP --durations=5

tests: docker-images
	docker run -it --rm -v $(PWD):/src $(DEV_IMAGE) \
	  $(PYTEST) --ignore docs

watch-tests: docker-images
	rm -f src/.testmondata
	docker run -it --rm -v $(PWD):/src $(DEV_IMAGE) \
	  ptw --runner "$(PYTEST) --testmon" --ignore docs
	rm -f src/.testmondata

bash-tests: docker-images
	docker run -it --rm -v $(PWD):/src $(DEV_IMAGE) bash
 