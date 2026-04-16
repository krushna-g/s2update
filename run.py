from S2Digital import create_app
import os

config = os.environ.get("S2Digital_CONFIG")  # e.g. S2Digital.config.ProdConfig
app = create_app(config)

if __name__ == "__main__":
   # app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", False))
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)