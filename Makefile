migration:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic revision --autogenerate && \
		sudo chown -R $(USER):$(USER) ./src/alembic

migration-apply:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic upgrade head