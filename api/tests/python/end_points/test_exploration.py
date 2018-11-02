
def test_explore(client, jwt, app, db):
    from namex.models import Request as RequestDAO, Event as EventDAO

    lines = filter(None, open('tests/data/src/requests.data').read().splitlines())
    for line in lines:
        columns = line.split('|')
        nr = RequestDAO()
        nr.id = columns[0].strip()
        nr.nrNum = columns[1].strip()
        nr.lastUpdate = columns[2].strip()
        nr.stateCd = columns[3].strip()
        nr.priorityCd = columns[4].strip()
        nr.save_to_db()
    (count,) = db.session.execute("SELECT count(id) as count FROM requests").first()
    assert count == 50

    (priorityRequests,) = db.session.execute("SELECT count(id) as count FROM requests where state_cd='DRAFT' and priority_cd='Y'").first()
    assert priorityRequests == 17

    (notExamined,) = db.session.execute("SELECT count(id) as count FROM requests where state_cd='HOLD'").first()
    assert notExamined == 18

    lines = filter(None, open('tests/data/src/events.data').read().splitlines())
    for line in lines:
        columns = line.split('|')
        e = EventDAO()
        e.nr_id = columns[0].strip()
        e.action = columns[1].strip()
        e.stateCd = columns[2].strip()
        e.eventDate = columns[3].strip()
        e.save_to_db()
    (count,) = db.session.execute("SELECT count(id) as count FROM events").first()
    assert count == 20

def test_insert_requests_and_events(client, jwt, app, db):
    from .postgres import Postgres

    lines = filter(None, open('tests/data/src/requests.data').read().splitlines())
    for line in lines:
        columns = line.split('|')
        Postgres().execute('INSERT INTO requests(id, nr_num, last_update, state_cd, priority_cd, submitted_date) values(%s,%s,%s,%s,%s,%s);',
                           (columns[0].strip(), columns[1].strip(), columns[2].strip(), columns[3].strip(), columns[4].strip(), columns[5].strip() ))
    (count,) = db.session.execute("SELECT count(id) as count FROM requests").first()
    assert count == 94

    lines = filter(None, open('tests/data/src/events.data').read().splitlines())
    for line in lines:
        columns = line.split('|')
        Postgres().execute('INSERT INTO events(nr_id, action, state_cd, event_dt) values(%s,%s,%s,%s);',
                           (columns[0].strip(), columns[1].strip(), columns[2].strip(), columns[3].strip()))
    (count,) = db.session.execute("SELECT count(id) as count FROM events").first()
    assert count == 20



