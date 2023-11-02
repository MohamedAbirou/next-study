from vercel.resources.base import Resource


class DnsRecord(Resource):
    def __init__(self, id, domain_name):
        self.id = id
        self.domain_name = domain_name

    @classmethod
    def get(cls, domain_name, record_id):
        return cls(id=record_id, domain_name=domain_name)

    @classmethod
    def create(
        cls,
        domain_name,
        name,
        type,
        value,
        ttl=None,
        api_version="v2",
        api_token=None,
        team_id=None,
    ):
        data = {"name": name, "type": type, "value": value}

        if ttl is not None:
            data["ttl"] = ttl

        res = cls.make_request(
            method="POST",
            resource=f"/{api_version}/domains/{domain_name}/records",
            data=data,
            api_token=api_token,
            team_id=team_id,
        )

        return cls(id=res["uid"], domain_name=domain_name)

    @classmethod
    def list_records(
        cls,
        domain_name,
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

        res = cls.make_paginated_request(
            resource=f"/{api_version}/domains/{domain_name}/records",
            response_key="records",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res

    @classmethod
    def delete(
        cls, domain_name, record_id, api_version="v2", api_token=None, team_id=None
    ):
        return cls.make_request(
            method="DELETE",
            resource=f"/{api_version}/domains/{domain_name}/records/{record_id}",
            api_token=api_token,
            team_id=team_id,
        )
