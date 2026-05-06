FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir build wheel
RUN pip install -r requirements.txt
RUN pip install .

CMD ["python", "quantum_experiments/run_all_experiments.py"]
