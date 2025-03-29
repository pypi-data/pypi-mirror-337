import pytest
import requests
from jwskate import InvalidJwk, Jwk
from requests_mock import ANY

from requests_oauth2client import (
    ClientSecretBasic,
    ClientSecretJwt,
    ClientSecretPost,
    InvalidClientAssertionSigningKeyOrAlg,
    InvalidRequestForClientAuthentication,
    OAuth2Client,
    PrivateKeyJwt,
    UnsupportedClientCredentials,
)
from tests.conftest import RequestsMocker, RequestValidatorType


def test_client_secret_post(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    client_secret: str,
    client_secret_post_auth_validator: RequestValidatorType,
) -> None:
    client = OAuth2Client(token_endpoint, ClientSecretPost(client_id, client_secret))

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    client_secret_post_auth_validator(requests_mock.last_request, client_id=client_id, client_secret=client_secret)


def test_client_secret_basic(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    client_secret: str,
    client_secret_basic_auth_validator: RequestValidatorType,
) -> None:
    client = OAuth2Client(token_endpoint, ClientSecretBasic(client_id, client_secret))

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    client_secret_basic_auth_validator(requests_mock.last_request, client_id=client_id, client_secret=client_secret)


def test_private_key_jwt(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    private_jwk: Jwk,
    private_key_jwt_auth_validator: RequestValidatorType,
    public_jwk: Jwk,
) -> None:
    client = OAuth2Client(token_endpoint, PrivateKeyJwt(client_id, private_jwk=private_jwk))

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    private_key_jwt_auth_validator(
        requests_mock.last_request,
        client_id=client_id,
        public_jwk=public_jwk,
        endpoint=token_endpoint,
    )

    with pytest.raises(ValueError, match="asymmetric private signing key") as exc:
        PrivateKeyJwt(client_id, private_jwk.public_jwk())
    assert exc.type is InvalidClientAssertionSigningKeyOrAlg


def test_private_key_jwt_with_kid(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    private_jwk: Jwk,
    private_key_jwt_auth_validator: RequestValidatorType,
    public_jwk: Jwk,
) -> None:
    client = OAuth2Client(token_endpoint, PrivateKeyJwt(client_id, private_jwk=private_jwk))

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    private_key_jwt_auth_validator(
        requests_mock.last_request,
        client_id=client_id,
        public_jwk=public_jwk,
        endpoint=token_endpoint,
    )


def test_client_secret_jwt(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    client_secret: str,
    client_secret_jwt_auth_validator: RequestValidatorType,
) -> None:
    client = OAuth2Client(token_endpoint, ClientSecretJwt(client_id, client_secret))

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    client_secret_jwt_auth_validator(
        requests_mock.last_request,
        client_id=client_id,
        client_secret=client_secret,
        endpoint=token_endpoint,
    )


def test_public_client(
    requests_mock: RequestsMocker,
    access_token: str,
    token_endpoint: str,
    client_id: str,
    target_api: str,
    public_app_auth_validator: RequestValidatorType,
) -> None:
    client = OAuth2Client(token_endpoint, client_id)

    requests_mock.post(
        token_endpoint,
        json={"access_token": access_token, "token_type": "Bearer", "expires_in": 3600},
    )

    assert client.client_credentials()
    assert requests_mock.called_once
    public_app_auth_validator(requests_mock.last_request, client_id=client_id)


def test_invalid_request(requests_mock: RequestsMocker, client_id: str, client_secret: str) -> None:
    requests_mock.get(ANY)
    with pytest.raises(RuntimeError) as exc:
        requests.get("http://localhost", auth=ClientSecretBasic(client_id, client_secret))
    assert exc.type is InvalidRequestForClientAuthentication


def test_private_key_jwt_missing_alg(client_id: str, private_jwk: Jwk) -> None:
    private_jwk_without_alg = dict(private_jwk)
    private_jwk_without_alg.pop("alg")
    with pytest.raises(ValueError) as exc:
        PrivateKeyJwt(client_id=client_id, private_jwk=private_jwk_without_alg, alg=None)
    assert exc.type is InvalidClientAssertionSigningKeyOrAlg


def test_private_key_jwt_unsupported_alg(client_id: str, private_jwk: Jwk) -> None:
    private_jwk_without_alg = dict(private_jwk)
    private_jwk_without_alg.pop("alg")
    with pytest.raises(ValueError) as exc:
        PrivateKeyJwt(client_id=client_id, private_jwk=private_jwk_without_alg, alg="FOO")
    assert exc.type is InvalidClientAssertionSigningKeyOrAlg


def test_private_key_jwt_missing_kid(client_id: str, private_jwk: Jwk) -> None:
    private_jwk_without_kid = dict(private_jwk)
    private_jwk_without_kid.pop("kid")
    with pytest.raises(ValueError) as exc:
        PrivateKeyJwt(client_id=client_id, private_jwk=private_jwk_without_kid)
    assert exc.type is InvalidClientAssertionSigningKeyOrAlg


def test_init_auth(token_endpoint: str, client_id: str, client_secret: str, private_jwk: Jwk) -> None:
    csp_client = OAuth2Client(token_endpoint, (client_id, client_secret))
    assert isinstance(csp_client.auth, ClientSecretPost)
    assert csp_client.auth.client_id == client_id
    assert csp_client.auth.client_secret == client_secret

    pkj_client = OAuth2Client(token_endpoint, (client_id, dict(private_jwk)))
    assert isinstance(pkj_client.auth, PrivateKeyJwt)
    assert pkj_client.auth.client_id == client_id
    assert pkj_client.auth.private_jwk == private_jwk

    with pytest.raises(ValueError, match="must have a Key Type") as exc:
        OAuth2Client(token_endpoint, (client_id, {"foo": "bar"}))
    assert exc.type is InvalidJwk

    with pytest.raises(TypeError, match="not supported") as exc2:
        OAuth2Client(token_endpoint, (client_id, object()))  # type: ignore[arg-type]
    assert exc2.type is UnsupportedClientCredentials
