import ast
import numpy as np
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
        coordinates = ast.literal_eval(bounding_box.coordinates)
        samples = ast.literal_eval(bounding_box.samples)
        googlescores, googletags = hmu.getGoogleData(
            np.asarray(samples['xvals']),
            np.asarray(samples['yvals']),
            int(samples['num_xsamples']),
            int(samples['num_ysamples'])
        )

        db_session.refresh(bounding_box)
        list_googlescores = {
            tag: scores.tolist() for tag, scores in googlescores.items()
        }
        bounding_box.googletags = str(googletags)
        bounding_box.googlescores = str(list_googlescores)
        bounding_box.state = 'ready'
        db_session.commit()
        return googletags
    except Exception as exc:
        print(exc)
        return {}
