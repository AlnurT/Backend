from app.services.auth import AuthServices


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    encoded_jwt = AuthServices.create_access_token(data)

    assert encoded_jwt
    assert isinstance(encoded_jwt, str)

    payload = AuthServices.decode_token(encoded_jwt)
    assert payload
    assert payload["user_id"] == data["user_id"]
