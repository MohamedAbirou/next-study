from vercel.resources.base import Resource


class Certificate(Resource):
    def __init__(self, id, cns, created, expiration, auto_renew):
        self.id = id
        self.cns = cns
        self.created = created
        self.expiration = expiration
        self.auto_renew = auto_renew

    @classmethod
    def from_data(cls, data):
        return cls(
            id=data["uid"],
            cns=data["cns"],
            created=data["created"],
            expiration=data["expiration"],
            auto_renew=data["autoRenew"],
        )

    @classmethod
    def create(cls, domains, api_version="v3", api_token=None, team_id=None):
        return cls.make_request(
            method="POST",
            resource=f"/{api_version}/now/certs",
            data={"domains": domains},
            api_token=api_token,
            team_id=team_id,
        )

    @classmethod
    def submit(cls, ca, cert, key, api_version="v3", api_token=None, team_id=None):
        return cls.make_request(
            method="PUT",
            resource=f"/{api_version}/now/certs",
            data={"ca": ca, "cert": cert, "key": key},
            api_token=api_token,
            team_id=team_id,
        )

    @classmethod
    def get(cls, certificate_id, api_version="v3", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}/now/certs/{certificate_id}",
            api_token=api_token,
            team_id=team_id,
        )

        return cls.from_data(res)

    def delete(self, api_version="v3", api_token=None, team_id=None):
        return self.make_request(
            method="DELETE",
            resource=f"/{api_version}/now/certs/{self.id}",
            api_token=api_token,
            team_id=team_id,
        )
