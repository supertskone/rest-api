# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install fastapi[all] sqlalchemy

# Create database tables
python -c "
from database import engine
import models
models.Base.metadata.create_all(bind=engine)
"

# Install additional testing dependencies
pip install pytest httpx

# Populate the database and run the app
python populate_db.py
uvicorn main:app --reload
