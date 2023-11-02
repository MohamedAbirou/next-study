from vercel.resources.base import Resource


class User(Resource):
    def __init__(self):
        pass

    @classmethod
    def from_data(cls, data):
        return cls()

    @classmethod
    def get(cls, api_version="", api_token=None, team_id=None):
        res = cls.make_request(
            method="GET",
            resource=f"/{api_version}www/user",  # no trailing slash because no api version
            api_token=api_token,
            team_id=team_id,
        )

        return res
