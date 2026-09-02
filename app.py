import os
from core.factory import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(host="127.0.0.1", port=port, debug=True)
