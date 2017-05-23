from celery import Celery
from location_tool.database import db_session
from location_tool import models
import location_tool.heat_map_utils as hmu

app = Celery('tasks')
app.config_from_object('location_tool.celeryconfig')

@app.task
def get_google_data(bounding_box_id):
    bounding_box = db_session.query(models.BoundingBox).get(bounding_box_id)
    try:
        data = hmu.prepare_query(bounding_box)
        googlescores, googletags = hmu.getGoogleData(
            data['xvals'],
            data['yvals'],
            data['num_xsamples'],
            data['num_ysamples']
        )
        output_google = hmu.javascriptwriter(
            googlescores,
            data['xvals'],
            data['yvals'],
            data['num_xsamples'],
            data['num_ysamples'],
            googletags
        )
    except Exception as exc:
        print(exc.message)
        output_google = None

    db_session.refresh(bounding_box)
    bounding_box.output_google = output_google
    db_session.commit()
