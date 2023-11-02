from vercel.resources.base import Resource


class Deployment(Resource):
    def __init__(
        self,
        aliases,
        alias_assigned,
        alias_error,
        created_at,
        created_in,
        deployment_hostname,
        forced,
        id,
        meta,
        plan,
        private,
        ready_state,
        requested_at,
        target,
        team_id,
        type,
        url,
        user_id,
        regions,
        functions,
        routes,
        env,
        build,
        version,
        name,
        public,
        owner_id,
    ):
        self.aliases = aliases
        self.alias_assigned = alias_assigned
        self.alias_error = alias_error
        self.created_at = created_at
        self.created_in = created_in
        self.deployment_hostname = deployment_hostname
        self.forced = forced
        self.id = id
        self.meta = meta
        self.plan = plan
        self.private = private
        self.ready_state = ready_state
        self.requested_at = requested_at
        self.target = target
        self.team_id = team_id
        self.type = type
        self.url = url
        self.user_id = user_id
        self.version = version
        self.regions = regions
        self.functions = functions
        self.routes = routes
        self.env = env
        self.build = build
        self.version = version
        self.name = name
        self.public = public
        self.owner_id = owner_id

    @classmethod
    def from_data(cls, data):
        aliases = data.get("alias", [])

        return cls(
            aliases=aliases,
            alias_assigned=data["aliasAssigned"],
            alias_error=data.get("aliasError"),
            created_at=data["createdAt"],
            created_in=data["createdIn"],
            deployment_hostname=data.get("deploymentHostname"),
            forced=data.get("forced"),
            id=data["id"],
            meta=data["meta"],
            plan=data["plan"],
            private=data.get("private"),
            ready_state=data["readyState"],
            requested_at=data.get("requestedAt"),
            target=data.get("target"),
            team_id=data.get("teamId"),
            type=data.get("type"),
            url=data["url"],
            user_id=data.get("userId"),
            regions=data.get("regions", []),
            functions=data.get("functions"),
            routes=data.get("routes"),
            env=data.get("env", []),
            build=data.get("build", {"env": {}}),
            version=data.get("version"),
            name=data.get("name"),
            public=data.get("public"),
            owner_id=data.get("ownerId"),
        )

    @classmethod
    def get(
        cls,
        deployment_id=None,
        deployment_url=None,
        api_version="v11",
        api_token=None,
        team_id=None,
    ):
        if deployment_id is None and deployment_url is None:
            raise Exception("one of deployment_id or deployment_url is required")

        if deployment_id is not None and deployment_url is not None:
            raise Exception(
                "only one of deployment_id or deployment_url can be specified"
            )

        resource = "/now/deployments"
        if deployment_id is not None:
            resource += f"/{deployment_id}"

        params = {}
        if deployment_url is not None:
            params["url"] = deployment_url

        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}{resource}",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    def delete(self, url=None, api_version="v11", api_token=None, team_id=None):
        resource = f"/now/deployments/{self.id}"
        params = {}

        if url is not None:
            resource = "/now/deployments/remove"
            params["url"] = url

        return self.make_request(
            method="DELETE",
            resource=f"/{api_version}{resource}",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )

    def cancel(self, api_version="v12", api_token=None, team_id=None):
        res = self.make_request(
            method="PATCH",
            resource=f"/{api_version}/now/deployments/{self.id}/cancel",
            api_token=api_token,
            team_id=team_id,
        )
        # todo: refactor to update object rather than create a new one
        return Deployment.from_data(res)

    def list_aliases(
        self,
        limit=None,
        since=None,
        until=None,
        api_version="v2",
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
            resource=f"/{api_version}/now/deployments/{self.id}/aliases",
            response_key="aliases",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res
