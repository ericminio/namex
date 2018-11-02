from namex.models import db
import datetime

class DashboardService(object):

    def __init__(self):
        self.priorityRequestCount = 0

    @staticmethod
    def get_data():
        (priorityRequests,) = db.session.execute(
            "SELECT count(id) as count FROM requests where state_cd='DRAFT' and priority_cd='Y'").first()
        days = []

        try:
            days = db.session.execute(
                """
                    select 
                        id,
                        nr_id,
                        event_dt
                    into temporary candidates
                    from events
                    where
                        state_cd = 'DRAFT'
                        and nr_id in (
                            select id 
                            from requests r 
                            where r.state_cd='DRAFT' and r.priority_cd='N'
                        );
                    
                    select
                        nr_id,
                        min(event_dt) as event_dt
                    into temporary candidates_creation
                    from candidates
                    group by nr_id;
                    
                    SELECT 
                        event_dt::timestamp::date as day,
                        count(1) as count 
                    FROM candidates_creation
                    group by event_dt::timestamp::date
                    order by day desc;
                """
                ).fetchall()
            print(days)
            days = [{ 'date':day.strftime('%B %d'), 'count':count} for (day, count) in days]
        except Exception as e:
            print (e)
            raise e

        return {
            'priorityRequestCount':priorityRequests,
            'days': days
        }