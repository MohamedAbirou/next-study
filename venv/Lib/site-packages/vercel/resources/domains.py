from vercel.resources.base import Resource
from vercel.resources.dns import DnsRecord


class Price(Resource):
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period

    @classmethod
    def from_data(cls, name, data):
        return cls(name=name, price=data["price"], period=data["period"])

    def purchase(self, api_version="v4"):
        return Domain.purchase(name=self.name, expected_price=self.price)


class Creator:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @classmethod
    def from_data(cls, data):
        return cls(id=data["id"], username=data["username"], email=data["email"])


class Domain(Resource):
    def __init__(
        self,
        name,
        id,
        service_type,
        ns_verified_at,
        txt_verified_at,
        cdn_enabled,
        created_at,
        bought_at,
        transferred_at,
        verification_record,
        verified,
        nameservers,
        intended_nameservers,
        creator,
        suffix,
        aliases,
        certs,
    ):
        self.name = name
        self.id = id
        self.service_type = service_type
        self.ns_verified_at = ns_verified_at
        self.txt_verified_at = txt_verified_at
        self.cdn_enabled = cdn_enabled
        self.created_at = created_at
        self.bought_at = bought_at
        self.transferred_at = transferred_at
        self.verification_record = verification_record
        self.verified = verified
        self.nameservers = nameservers
        self.intended_nameservers = intended_nameservers
        self.creator = creator
        self.suffix = suffix
        self.aliases = aliases
        self.certs = certs

    @classmethod
    def from_data(cls, data):
        if "domain" in data:
            data = data["domain"]
        creator = data.get("creator")

        if creator is not None:
            creator = Creator.from_data(creator)

        return cls(
            name=data.get("name"),
            id=data.get("id"),
            service_type=data.get("serviceType"),
            ns_verified_at=data.get("nsVerifiedAt"),
            txt_verified_at=data.get("txtVerifiedAt"),
            cdn_enabled=data.get("cdnEnabled"),
            created_at=data.get("createdAt"),
            bought_at=data.get("boughtAt"),
            transferred_at=data.get("transferredAt"),
            verification_record=data.get("verificationRecord"),
            verified=data.get("verified"),
            nameservers=data.get("nameservers", []),
            intended_nameservers=data.get("intendedNameservers", []),
            creator=creator,
            suffix=data.get("suffix"),
            aliases=data.get("aliases", []),
            certs=data.get("certs", []),
        )

    @classmethod
    def list_all(
        cls,
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

        res = cls.make_paginated_request(
            resource=f"/{api_version}/domains",
            response_key="domains",
            params=params,
            api_token=api_token,
            team_id=team_id,
        )
        return res

    @classmethod
    def get(cls, name, api_version="v4", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/domains/{name}",
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    @classmethod
    def create(cls, name, api_version="v4", api_token=None, team_id=None):
        res = cls.make_request(
            method="POST",
            resource=f"/{api_version}/domains",
            data={"name": name},
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    @classmethod
    def check_availability(cls, name, api_version="v4", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/domains/status",
            params={"name": name},
            api_token=api_token,
            team_id=team_id,
        )

        return res

    @classmethod
    def check_price(cls, name, api_version="v4", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/domains/price",
            params={"name": name},
            api_token=api_token,
            team_id=team_id,
        )

        return Price.from_data(name, res)

    @classmethod
    def purchase(
        cls, name, expected_price, api_version="v4", api_token=None, team_id=None
    ):
        res = cls.make_request(
            method="POST",
            resource=f"/{api_version}/domains/buy",
            data={"name": name, "expectedPrice": expected_price},
            api_token=api_token,
            team_id=team_id,
        )

        return res

    def delete(self, api_version="v4", api_token=None, team_id=None):
        return self.make_request(
            method="DELETE",
            resource=f"/{api_version}/domains/{self.name}",
            api_token=api_token,
            team_id=team_id,
        )

    def create_dns_record(self, name, type, value, ttl=None):
        return DnsRecord.create(
            domain_name=self.name, name=name, type=type, value=value, ttl=ttl
        )

    def get_dns_record(self, record_id):
        return DnsRecord.get(domain_name=self.name, record_id=record_id)

    def list_records(self, limit=None, since=None, until=None):
        return DnsRecord.list_records(
            domain_name=self.name, limit=limit, since=since, until=until
        )
