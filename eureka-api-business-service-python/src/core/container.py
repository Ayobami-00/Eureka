from dependency_injector import containers, providers

from src.core.config import settings
from src.database.db import Database
from src.repository import *
from src.usecase import *


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.gapi.business_service",
            # "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=settings.DATABASE_URI)

    business_repository = providers.Factory(BusinessRepository, session_factory=db.provided.session)
    
    business_usecase = providers.Factory(BusinessUsecase, business_repository=business_repository)
