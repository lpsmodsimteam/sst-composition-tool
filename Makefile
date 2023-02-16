docker_build:
	docker build --tag composition_demo -f Dockerfile

docker_run:
	docker run -it --rm composition_demo /bin/bash


apptainer_build:
	appraiser build demo.sif demo.def

apptainer_shell:
	appraiser shell demo.sif

