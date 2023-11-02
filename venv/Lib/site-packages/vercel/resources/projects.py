from vercel.resources.base import Resource
from vercel.resources.deployments import Deployment


class ProjectAlias:
    def __init__(
        self, domain, target, created_at, configured_by, configured_changed_at
    ):
        self.domain = domain
        self.target = target
        self.created_at = created_at
        self.configured_by = configured_by
        self.configured_changed_at = configured_changed_at

    @classmethod
    def from_data(cls, data):
        return cls(
            domain=data["domain"],
            target=data["target"],
            created_at=data["createdAt"],
            configured_by=data["configuredBy"],
            configured_changed_at=data["configuredChangedAt"],
        )


class EnvironmentVariable(Resource):
    def __init__(
        self, project_id, key, value, configuration_id, updated_at, created_at
    ):
        self.project_id = project_id
        self.key = key
        self.value = value
        self.configuration_id = configuration_id
        self.updated_at = updated_at
        self.created_at = created_at

    @classmethod
    def from_data(cls, project_id, data):
        return cls(
            project_id=project_id,
            key=data["key"],
            value=data["value"],
            configuration_id=data["configurationId"],
            updated_at=data["updatedAt"],
            created_at=data["createdAt"],
        )


class Project(Resource):
    def __init__(
        self,
        id,
        name,
        aliases,
        account_id,
        updated_at,
        created_at,
        latest_deployments,
        production_deployment,
        environment_variables,
    ):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.account_id = account_id
        self.updated_at = updated_at
        self.created_at = created_at
        self.latest_deployments = latest_deployments
        self.production_deployment = production_deployment
        self.environment_variables = environment_variables

    def update_from_data(self, data):
        return self

    @classmethod
    def from_data(cls, data):
        project_id = data["id"]

        # Aliases
        aliases = [ProjectAlias.from_data(alias) for alias in data.get("alias", [])]

        # Production Deployment
        target = data.get("targets", {})
        production = target.get("production")

        if production is not None:
            production = Deployment.from_data(production)

        # Environment Variables
        environment_variables = [
            EnvironmentVariable.from_data(project_id, env)
            for env in data.get("env", [])
        ]

        # Latest Deployments
        latest_deployments = [
            Deployment.from_data(deployment)
            for deployment in data.get("latestDeployments", [])
        ]

        return cls(
            id=project_id,
            name=data["name"],
            aliases=aliases,
            account_id=data["accountId"],
            updated_at=data["updatedAt"],
            created_at=data["createdAt"],
            latest_deployments=latest_deployments,
            production_deployment=production,
            environment_variables=environment_variables,
        )

    @classmethod
    def get(cls, identifier, api_version="v1", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/projects/{identifier}",
            api_token=api_token,
            team_id=team_id,
        )
        return cls.from_data(res)

    @classmethod
    def create(cls, name, api_version="v1", api_token=None, team_id=None):
        res = cls.make_request(
            method="POST",
            resource=f"/{api_version}/projects",
            data={"name": name},
            team_id=team_id,
        )
        return cls.from_data(res)

    def delete(self, api_version="v1", api_token=None, team_id=None):
        return self.make_request(
            method="DELETE",
            resource=f"/{api_version}/projects/{self.id}",
            api_token=api_token,
            team_id=team_id,
        )

    # def get_environment_variables(self, api_version='v5'):
    #     res = cls.make_request(
    #       method='GET',
    #       resource=f'/projects/{self.id}/env',
    #       api_version=api_version
    #     )

    #     return res

    def create_environment_variable(
        self, key, value, target, api_version="v4", api_token=None, team_id=None
    ):
        # validate target

        res = self.make_request(
            method="POST",
            resource=f"/{api_version}/projects/{self.id}/env",
            data={"key": key, "value": value, "target": target},
            api_token=api_token,
            team_id=team_id,
        )

        return EnvironmentVariable.from_data(self.id, res)

    def delete_environment_variable(
        self, key, target, api_version="v4", api_token=None, team_id=None
    ):
        # validate target

        res = self.make_request(
            method="DELETE",
            resource=f"/{api_version}/projects/{self.id}/env/{key}",
            params={"target": target},
            api_token=api_token,
            team_id=team_id,
        )

        return EnvironmentVariable.from_data(self.id, res)

    def add_domain(
        self, domain, redirect=None, api_version="v1", api_token=None, team_id=None
    ):
        data = {"domain": domain}

        if redirect is not None:
            data["redirect"] = redirect

        res = self.make_request(
            method="POST",
            resource=f"/{api_version}/projects/{self.id}/alias",
            data=data,
            api_token=api_token,
            team_id=team_id,
        )

        return res

    def redirect_domain(
        self, domain, redirect=None, api_version="v1", api_token=None, team_id=None
    ):
        data = {"domain": domain}

        if redirect is not None:
            data["redirect"] = redirect

        res = self.make_request(
            method="PATCH",
            data=data,
            resource=f"/{api_version}/projects/{self.id}/alias",
            api_token=api_token,
            team_id=team_id,
        )

        return

    def remove_domain(self, domain, api_version="v1", api_token=None, team_id=None):
        res = self.make_request(
            method="DELETE",
            resource=f"/{api_version}/projects/{self.id}/alias",
            params={"domain": domain},
            api_token=api_token,
            team_id=team_id,
        )

        return res

    @classmethod
    def list_all(
        cls,
        search=None,
        limit=None,
        since=None,
        until=None,
        api_version="v4",
        api_token=None,
        team_id=None,
    ):
        params = {}

        if limit is not None:
            params["limit"] = limit

        if since is not None:
            params["since"] = since

        if until is not None:
            params["until"] = until

        if search is not None:
            params["search"] = search

        res = cls.make_paginated_request(
            resource=f"/{api_version}/projects",
            response_key="projects",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res

    def list_environment_variables(
        self,
        limit=None,
        since=None,
        until=None,
        api_version="v5",
        api_token=None,
        team_id=None,
    ):
        params = {}

        if limit is not None:
            params["limit"] = limit

        if since is not None:
            params["since"] = since

        if until is not None:
            params["until"] = until

        res = self.make_paginated_request(
            resource=f"/{api_version}/projects/{self.id}/env",
            response_key="envs",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res
