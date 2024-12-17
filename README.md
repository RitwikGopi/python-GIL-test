# Setup

- Setup a venv for better experience.
- Install requirements `pip install -r requirements.txt`
- Run server `.venv/bin/gunicorn -b 0.0.0.0:5000 --workers=4 --threads=1  --capture-output --access-logfile - server:app`
- Run the performance measuring script `python main.py`