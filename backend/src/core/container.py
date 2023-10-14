from dependency_injector import containers, providers

from core.config import SQL_DATABASE_URL
from core.database import Database
from repository import DisciplineRepository, TournamentRepository, UserRepository
from service import AuthService, DisciplineService, TournamentService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.endpoints.auth_router",
            "api.v1.endpoints.tournament_router",
            "api.v1.endpoints.user_router",
            "api.v1.endpoints.discipline_router",
            "core.dependencies",
        ]
    )

    db: Database = providers.Singleton(Database, db_url=SQL_DATABASE_URL)

    user_repository: UserRepository = providers.Factory(
        UserRepository, session_factory=db.provided.session
    )

    discipline_repository: DisciplineRepository = providers.Factory(
        DisciplineRepository, session_factory=db.provided.session
    )

    tournament_repository: TournamentRepository = providers.Factory(
        TournamentRepository, session_factory=db.provided.session
    )

    auth_service: AuthService = providers.Factory(
        AuthService, user_repository=user_repository
    )

    discipline_service: DisciplineService = providers.Factory(
        DisciplineService, discipline_repository=discipline_repository
    )

    user_service: UserService = providers.Factory(
        UserService, user_repository=user_repository
    )

    tournament_service: TournamentService = providers.Factory(
        TournamentService, tournament_repository=tournament_repository
    )
