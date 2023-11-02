import requests
import vercel
from vercel.exceptions import VercelError


class Resource:
    @staticmethod
    def _make_request(url, method, headers, params, data=None):
        try:
            kwargs = dict(url=url, method=method, headers=headers, params=params)

            if data is not None:
                kwargs["json"] = data

            response = requests.request(**kwargs).json()

            if "error" in response:
                raise VercelError(
                    code=response["error"]["code"], message=response["error"]["message"]
                )

            return response
        except Exception as e:
            raise e

    @classmethod
    def make_request(
        cls,
        method,
        resource,
        data=None,
        headers=None,
        params=None,
        api_token=None,
        team_id=None,
    ):
        if api_token is None:
            api_token = vercel.api_token

        if team_id is None:
            team_id = vercel.team_id

        if api_token is None:
            raise Exception(f"api_token was not found")

        if params is None:
            params = {}

        if headers is None:
            headers = {}

        try:
            base_url = "api.vercel.com"
            url = f"https://{base_url}{resource}"

            headers.update(
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_token}",
                }
            )

            if team_id is not None:
                params.update({"teamId": team_id})

            response = cls._make_request(
                url=url, method=method, headers=headers, params=params, data=data
            )

            return response
        except Exception as e:
            raise e

    @classmethod
    def make_paginated_request(
        cls,
        resource,
        response_key,
        method="GET",
        headers=None,
        params=None,
        api_token=None,
        team_id=None,
        results=None,
    ):
        if results is None:
            results = []

        if params is None:
            params = {}

        if headers is None:
            headers = {}

        if api_token is None:
            api_token = vercel.api_token

        if api_token is None:
            raise Exception(f"api_token was not found")

        # Add Authentication Headers
        headers.update(
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_token}",
            }
        )

        if team_id is None:
            team_id = vercel.team_id

        # Add Team ID if set
        if team_id is not None:
            params.update({"teamId": team_id})

        base_url = "api.vercel.com"

        try:
            url = f"https://{base_url}{resource}"

            response = cls._make_request(
                url=url, method=method, headers=headers, params=params
            )

            # Append records to results
            records = response.get(response_key)
            if records is None:
                raise ValueError("unable to find records for responsekey")
            results += records

            pagination = response.get("pagination")

            while pagination is not None:
                next_params = params.copy()

                # Update Next Parameter
                next_params.update({"since": pagination["next"]})
                response = cls._make_request(
                    url=url, method=method, headers=headers, params=next_params
                )

                # Append records to results
                records = response.get(response_key)
                if records is None:
                    raise ValueError("unable to find records for responsekey")
                results += records

                pagination = response.get("pagination")
            return results
        except Exception as e:
            raise e
