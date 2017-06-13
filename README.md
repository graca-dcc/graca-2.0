# graca2.0

sudo apt-get install python-dev libffi-dev libssl-dev
virtualenv venv
source env.sh
pip install -r requirements.txt

# regenerate pickle files (optional)

python generate_pickle.py


# run demo

python demo.py
