from flask import jsonify
from unittest import mock
import sys
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
def seed_database_with(requests=[]):
    from namex.models import Request as RequestDAO

    for request in requests:
        nr = RequestDAO()
        nr.id = request[0]
        nr.nrNum = 'NR ' + str(request[0])
        nr.stateCd = request[1]
        nr.priorityCd = request[2]
        nr.submittedDate = request[3]
        nr.save_to_db()


def get_dashboard_data(client, jwt):
    import json
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    rv = client.get('/api/v1/requests/dashboard', headers=headers)
    data = json.loads(rv.data)
    return data

def get_dashboard_data_having_database_seeded_with(client, jwt, requests=[]):
    seed_database_with(requests)
    return get_dashboard_data(client, jwt)

def verify_given_days_equals(data, expected):
    print(data['days'])
    assert expected == data['days']

def verify_given_data_produces_expected_dashboard(client, jwt, requests=[], expected=[]):
    data = get_dashboard_data_having_database_seeded_with(client, jwt, requests)
    verify_given_days_equals(data, expected)

def test_get_dashboard_priority_request(client, jwt, app):
    data = get_dashboard_data_having_database_seeded_with(client, jwt,
        requests=[
            [1, 'DRAFT', 'Y', '2018-10-19 22:00:00'],
            [2, 'DRAFT', 'N', '2018-10-19 22:00:00'],
            [3, 'HOLD', 'Y', '2018-10-19 22:00:00']
        ]
    )

    assert data['priorityRequestCount'] == 1
    assert data['days'] == [{'date': 'October 19', 'count': 1}]


def test_get_dashboard_day_one(client, jwt, app):
    verify_given_data_produces_expected_dashboard(client, jwt,
        requests=[
            [1, 'DRAFT', 'N', '2018-10-19 22:00:00']
        ],
        expected=[
            {'date': 'October 19', 'count': 1}
        ]
    )

def test_get_dashboard_day_one_with_count_two(client, jwt, app):
    verify_given_data_produces_expected_dashboard(client, jwt,
        requests=[
            [1, 'DRAFT', 'N', '2018-10-19 22:00:00'],
            [2, 'DRAFT', 'N', '2018-10-19 21:00:00']
        ],
        expected=[
            {'date': 'October 19', 'count': 2}
        ]
    )

def test_get_dashboard_two_days(client, jwt, app):
    verify_given_data_produces_expected_dashboard(client, jwt,
        requests=[
            [1, 'DRAFT', 'N', '2018-10-20 22:00:00'],
            [2, 'DRAFT', 'N', '2018-10-20 21:00:00'],
            [3, 'DRAFT', 'N', '2018-10-21 21:00:00']
        ],
        expected=[
            {'date': 'October 21', 'count': 1},
            {'date': 'October 20', 'count': 2}
        ]
    )

def test_ignore_draft_now_with_priority_y(client, jwt, app):
    verify_given_data_produces_expected_dashboard(client, jwt,
        requests=[
            [1, 'DRAFT', 'Y', '2018-10-20 22:00:00']
        ],
        expected=[
        ]
    )

def test_ignore_draft_became_something_else(client, jwt, app):
    verify_given_data_produces_expected_dashboard(client, jwt,
        requests=[
            [1, 'APPROVED', 'N', '2018-10-20 22:00:00']
        ],
        expected=[
        ]
    )
