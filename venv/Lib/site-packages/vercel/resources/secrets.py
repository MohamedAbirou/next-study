from vercel.resources.base import Resource


class Secret(Resource):
    def __init__(self, id, name, value, team_id, user_id, created, created_at):
        self.id = id
        self.name = name
        self.value = value
        self.team_id = team_id
        self.user_id = user_id
        self.created = created
        self.created_at = created_at

    @classmethod
    def from_data(cls, data):
        return cls(
            id=data["uid"],
            name=data["name"],
            value=data.get("value"),
            team_id=data.get("teamId"),
            user_id=data["userId"],
            created=data["created"],
            created_at=data.get("createdAt"),
        )

    @classmethod
    def get(cls, identifier, api_version="v3", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/now/secrets/{identifier}",
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    @classmethod
    def create(cls, name, value, api_version="v2", api_token=None, team_id=None):
        res = cls.make_request(
            method="POST",
            resource=f"/{api_version}/now/secrets",
            data={"name": name, "value": value},
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    def delete(self, api_version="v2", api_token=None, team_id=None):
        return self.make_request(
            method="DELETE",
            resource=f"/{api_version}/now/secrets/{self.id}",
            api_token=api_token,
            team_id=team_id,
        )

    def update_name(self, name, api_version="v2", api_token=None, team_id=None):
        res = self.make_request(
            method="PATCH",
            resource=f"/{api_version}/now/secrets/{self.id}",
            data={"name": name},
            api_token=api_token,
            team_id=team_id,
        )
        self.name = res["name"]
        return self

    @classmethod
    def list_all(
        cls,
        limit=None,
        since=None,
        until=None,
        api_version="v3",
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

        res = cls.make_paginated_request(
            resource=f"/{api_version}/now/secrets",
            response_key="secrets",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res
