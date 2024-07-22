source venv/bin/activate
cd open-api
npm install
npm run generate-python && npm run generate-typescript

cd generated/pathological-python-api
pip install -r requirements.txt
pip install .
