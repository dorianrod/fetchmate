import os
from config import app

if __name__ == "__main__":
    import routes  # noqa: F401

    app.run(host="0.0.0.0", port=os.getenv("PORT", "5010"))
