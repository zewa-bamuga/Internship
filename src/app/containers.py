import logging

from dependency_injector import containers, providers
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import UnitOfWork
from a8t_tools.storage.facade import FileStorage
from a8t_tools.storage.local_storage import LocalStorageBackend
from a8t_tools.storage.s3_storage import S3StorageBackend
from a8t_tools.logging.utils import setup_logging

from app.config import Settings
from app.domain.storage.attachments.containers import AttachmentContainer
from app.domain.users.containers import UserContainer


class Container(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    config.from_dict(
        options=Settings(_env_file=".env", _env_file_encoding="utf-8").model_dump(),  # type: ignore [call-arg]
    )

    logging = providers.Resource(
        setup_logging,
        logger_level=logging.INFO,
        sentry_sdk=config.sentry.dsn,
        sentry_environment=config.sentry.env_name,
        sentry_traces_sample_rate=config.sentry.traces_sample_rate,
        json_logs=False,
    )

    transaction = providers.Singleton(AsyncDbTransaction, dsn=config.db.dsn)

    unit_of_work = providers.Factory(UnitOfWork, transaction=transaction)

    local_storage_backend = providers.Factory(
        LocalStorageBackend,
        base_path=config.storage.local_storage.base_path,
        base_uri=config.storage.local_storage.base_uri,
    )

    s3_storage_backend = providers.Factory(
        S3StorageBackend,
        s3_uri=config.storage.s3_storage.endpoint_uri,
        access_key_id=config.storage.s3_storage.access_key_id,
        secret_access_key=config.storage.s3_storage.secret_access_key,
        public_storage_uri=config.storage.s3_storage.public_storage_uri,
    )

    file_storage = providers.Factory(
        FileStorage,
        backend=providers.Callable(
            lambda use_s3, local_backend, s3_backendL: s3_backendL if (use_s3 is True) else local_backend,
            config.storage.use_s3,
            local_storage_backend,
            s3_storage_backend,
        ),
    )

    attachment = providers.Container(
        AttachmentContainer,
        transaction=transaction,
        file_storage=file_storage,
        bucket=config.storage.defauld_bucket,
    )

    user = providers.Container(
        UserContainer,
        transaction=transaction,
        secret_key=config.security.secret_key,
        private_key=config.security.private_key,
        public_key=config.security.public_key,
        pwd_context=config.security.pwd_context,
        access_expiration_time=config.security.access_expiration_min,
        refresh_expiration_time=config.security.refresh_expiration_min,
    )
