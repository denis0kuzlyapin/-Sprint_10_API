import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
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
    def create_offer(token, payload, image_path=None):
        fields = {
            "name": str(payload["name"]),
            "category": str(payload["category"]),
            "condition": str(payload["condition"]),
            "city": str(payload["city"]),
            "description": str(payload["description"]),
            "price": str(payload["price"]),
        }

        if image_path:
            with open(image_path, "rb") as image_file:
                multipart_data = MultipartEncoder(
                    fields={**fields, "images": ("image.jpg", image_file, "image/jpeg")}
                )

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": multipart_data.content_type,
                }

                return requests.post(
                    f"{Url.BASE_URL}{Endpoint.CREATE_OFFER}",
                    headers=headers,
                    data=multipart_data,
                )

        multipart_data = MultipartEncoder(fields=fields)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": multipart_data.content_type,
        }

        return requests.post(
            f"{Url.BASE_URL}{Endpoint.CREATE_OFFER}",
            headers=headers,
            data=multipart_data,
        )

    @staticmethod
    def change_data_offer(token, payload, offer_id, image_path=None):
        fields = {}

        for key, value in payload.items():
            if value is not None:
                fields[key] = str(value)

        if image_path:
            with open(image_path, "rb") as image_file:
                multipart_data = MultipartEncoder(
                    fields={**fields, "images": ("image.jpg", image_file, "image/jpeg")}
                )

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": multipart_data.content_type,
                }

                return requests.patch(
                    f"{Url.BASE_URL}{Endpoint.PATCH_OFFER}/{offer_id}",
                    headers=headers,
                    data=multipart_data,
                )

        multipart_data = MultipartEncoder(fields=fields)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": multipart_data.content_type,
        }

        return requests.patch(
            f"{Url.BASE_URL}{Endpoint.PATCH_OFFER}/{offer_id}",
            headers=headers,
            data=multipart_data,
        )

    @staticmethod
    def delete_offer(token, offer_id):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(
            f"{Url.BASE_URL}{Endpoint.DELETE_OFFER}/{offer_id}", headers=headers
        )
