from S2Digital import create_app
import os

config = os.environ.get("S2Digital_CONFIG")
app = create_app(config)
