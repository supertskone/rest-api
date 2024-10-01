python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install fastapi[all] sqlalchemy

python
>>> from database import engine
>>> import models
>>> models.Base.metadata.create_all(bind=engine)
>>> exit()

pip install pytest httpx
python populate_db.py
uvicorn main:app --reload