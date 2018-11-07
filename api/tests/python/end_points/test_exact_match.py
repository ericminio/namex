from namex.models import User

token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 31531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.EDITOR),
                    "{}".format(User.APPROVER),
                    "viewer",
                    "user"
                ]
            }
         }



def search_exact_match(client, jwt, query):
    import json
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    rv = client.get('/api/v1/exact-match', headers=headers)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    return data

def verify(data, expected):
    print(data['names'])
    assert expected == data['names']

def verify_exact_match_results(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    verify(data, expected)


def test_exact_match(client, jwt, app):
    verify_exact_match_results(client, jwt,
        query='JM Van Damme Inc',
        expected=[
            { 'name':'JM Van Damme Ltd' }
        ]
    )
