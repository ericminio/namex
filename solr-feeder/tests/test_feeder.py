from hamcrest import assert_that, equal_to
from .support_db import seed_conflicts, seed_names, read_all_seeds
from .support_solr import read_all_possible_conflicts
from solr_feeder.feeder import Feeder


def test_populates_possible_conflicts(db, solr):
    seed_conflicts(db, name='incredible name Inc', nr='123')
    Feeder(db, solr).go()
    conflicts = read_all_possible_conflicts(solr)

    assert_that(conflicts, equal_to([{'name': 'incredible name Inc'}]))


def test_does_not_possible_conflicts_when_core_target_is_names(db, solr):
    seed_names(db, name='incredible name Inc', nr='123')
    Feeder(db, solr).go()
    conflicts = read_all_possible_conflicts(solr)

    assert_that(conflicts, equal_to([]))


def test_ignores_conflict_with_status_completed(db, solr):
    seed_conflicts(db, name='incredible name Inc', nr='123', status='C')
    Feeder(db, solr).go()
    conflicts = read_all_possible_conflicts(solr)

    assert_that(conflicts, equal_to([]))


def test_updates_status_to_completed_when_done(db, solr):
    seed_conflicts(db, name='incredible name Inc', nr='123')
    seed = read_all_seeds(db)[0]
    assert_that(seed['status'], equal_to('P'))

    Feeder(db, solr).go()
    updated_seed = read_all_seeds(db)[0]
    assert_that(updated_seed['status'], equal_to('C'))


def test_deals_with_several_conflicts(db, solr):
    seed_conflicts(db, name='good', nr='111')
    seed_conflicts(db, name='crazy', nr='222')
    Feeder(db, solr).go()
    solr_names = read_all_possible_conflicts(solr)
    updated_seeds = read_all_seeds(db)

    assert_that(solr_names, equal_to([
        {'name': 'good'},
        {'name': 'crazy'}
    ]))
    assert_that(updated_seeds, equal_to([
        {'nr_num': '111', 'status': 'C'},
        {'nr_num': '222', 'status': 'C'}
    ]))
