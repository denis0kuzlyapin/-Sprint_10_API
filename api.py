import requests
from constants import Url, Endpoint


class User:

    @staticmethod
    def create_user(payload):
        return requests.post(f"{Url.BASE_URL}{Endpoint.USER_CREATE}", json=payload)

    @staticmethod
    def login(payload):
        return requests.post(f"{Url.BASE_URL}{Endpoint.LOGIN}", json=payload)


class Offer:

    @staticmethod
    def create_offer(token, payload):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.post(f"{Url.BASE_URL}{Endpoint.CREATE_OFFER}", headers=headers, json=payload)

    @staticmethod
    def change_data_offer(token, payload, offer_id):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.patch(
            f"{Url.BASE_URL}{Endpoint.PATCH_OFFER}/{offer_id}",
            headers=headers,
            json=payload,
        )

    @staticmethod
    def delete_offer(token, offer_id):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(
            f"{Url.BASE_URL}{Endpoint.DELETE_OFFER}/{offer_id}", headers=headers
        )
