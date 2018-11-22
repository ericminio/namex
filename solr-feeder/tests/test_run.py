import subprocess
from hamcrest import assert_that, equal_to
from .support_db import seed_conflicts, read_all_seeds
from .support_solr import read_all_possible_conflicts


def test_run_sh_exists():
    try:
        subprocess.call(['../run.sh'])
    except OSError as error:
        assert None == error


def test_runs_the_feeder(db, solr):
    seed_conflicts(db, name='good', nr='111')
    seed_conflicts(db, name='crazy', nr='222')
    try:
        subprocess.call(['../run.sh'])
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
    except OSError as error:
        assert None == error
