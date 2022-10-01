RUN=docker run -it --rm -p 5000:5000
DEV_IMAGE=doepy
docker-images: 
	docker build -t $(DEV_IMAGE) -f docker/Dockerfile.doepy .


PYTEST=pytest -o cache_dir=/tmp --testmon --quiet -rP --durations=5
watch-tests:
	rm -f src/.testmondata
	docker run -it --rm -v $(PWD):/src $(DEV_IMAGE) \
	  ptw --runner "$(PYTEST)" --ignore docs
	rm -f src/.testmondata

bash-tests:
	docker run -it --rm -v $(PWD):/src $(DEV_IMAGE) bash

# jupyter:
# 	docker run --rm -v $(PWD)/src:/src -p 8898:8898 $(JUPYTER_IMAGE) jupyter notebook --allow-root --port=8898 --ip 0.0.0.0 --no-browser


# isort:
# 	docker run -it --rm -v $(PWD)/src:/src $(DEV_IMAGE) isort mistat

# mypy:
# 	docker run -it --rm -v $(PWD)/src:/src $(DEV_IMAGE) mypy --install-types mistat

# pylint:
# 	docker run -it --rm -v $(PWD)/src:/src $(DEV_IMAGE) pylint mistat

# bash-dev:
# 	docker run -it --rm -v $(PWD)/src:/src $(DEV_IMAGE) bash