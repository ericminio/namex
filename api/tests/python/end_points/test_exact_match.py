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




def clean_database(client, jwt):
    import requests
    url = 'http://localhost:8983/solr/exact_match/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)
    assert r.status_code == 200

def seed_database_with(client, jwt, name):
    import requests
    url = 'http://localhost:8983/solr/exact_match/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"name":"' + name + '", "id":"1"}]'
    r = requests.post(url, headers=headers, data=data)
    assert r.status_code == 200

def verify(data, expected):
    print(data['names'])
    assert expected == data['names']

def verify_exact_match_results(client, jwt, query, expected):
    data = search_exact_match(client, jwt, query)
    verify(data, expected)


def search_exact_match(client, jwt, query):
    import json
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    rv = client.get('/api/v1/exact-match', headers=headers)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    return data

def test_exact_match(client, jwt, app):
    clean_database(client, jwt)
    seed_database_with(client, jwt, 'JM Van Damme Ltd')
    verify_exact_match_results(client, jwt,
        query='JM Van Damme Inc',
        expected=[
            { 'name':'JM Van Damme Ltd' }
        ]
    )
