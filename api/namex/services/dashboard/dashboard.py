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
                    SELECT 
                        submitted_date::timestamp::date as day,
                        count(1) as count 
                    FROM requests
                    where
                        state_cd = 'DRAFT'
                        and priority_cd = 'N'
                    group by submitted_date::timestamp::date
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