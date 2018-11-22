import os
import requests
import pytest
from hamcrest import assert_that, equal_to
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import TestConfig
from .support_solr import read_all_possible_conflicts, read_all_names


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(TestConfig)

    return app


@pytest.fixture(autouse=True)
def solr():
    return os.getenv('SOLR_TEST_URL') + '/solr'


@pytest.fixture(autouse=True)
def db(app):
    db = SQLAlchemy(app)
    background = [
        'drop table if exists solr_feeder;',
        """
        create table solr_feeder(
            id          varchar(10),
            nr_num      varchar(10),
            solr_core   varchar(10),
            action      varchar(10),
            status      varchar(10)
        );
        """,
        'drop schema if exists namex cascade;',
        'create schema namex;',
        """
        create table namex.solr_dataimport_names_vw(
            ID                  varchar(10),
            name_instance_id    varchar(10),
            choice_number       varchar(10),
            corp_num            varchar(10),
            NAME                varchar(100),
            nr_num              varchar(10),
            request_id          varchar(10),
            submit_count        varchar(10),
            request_type_cd     varchar(10),
            name_id             varchar(10),
            start_event_id      varchar(10),
            name_state_type_cd  varchar(10)
        );
        """,
        """
        create table namex.solr_dataimport_conflicts_vw(
            ID                  varchar(10),
            NAME                varchar(100),
            state_type_cd       varchar(10),
            SOURCE              varchar(10)
        );
        """
    ]
    for sql in background:
        db.engine.execute(sql)

    return db


@pytest.fixture(autouse=True)
def clear_solr_cores(solr):
    url = solr + '/possible.conflicts/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)
    assert_that(r.status_code, equal_to(200))

    url = solr + '/names/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)
    assert_that(r.status_code, equal_to(200))

    assert_that(read_all_names(solr), equal_to([]))
    assert_that(read_all_possible_conflicts(solr), equal_to([]))


