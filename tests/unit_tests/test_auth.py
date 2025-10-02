from app.services.auth import AuthServices


def test_create_access_token():
    data = {"user_id": 1}
    encoded_jwt = AuthServices.create_access_token(data)

    assert encoded_jwt
    assert isinstance(encoded_jwt, str)
