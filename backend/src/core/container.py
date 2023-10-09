from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.endpoints.authrouter",
            "api.v1.endpoints.tournament_router",
            "core.dependencies",
        ]
    )

    db = providers.Singleton()
