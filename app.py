from S2Digital import create_app
from S2Digital.extensions import db
import os

config = os.environ.get("S2Digital_CONFIG")
app = create_app(config)

with app.app_context():
    db.create_all()
