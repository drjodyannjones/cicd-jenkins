# Setup Virtual Environment

```python
conda create -n jenkins-env python=3.10 -y
conda activate jenkins-env
pip install -r requirements.txt
pip install .
```

# Docker commands

```
docker build -t loan_pred:v1 .
docker build -t drjodyannjones/cicd:latest .
docker push drjodyannjones/cicd:latest

# Create a container
docker run -d -it --name modelv1 -p 8005:8005 drjodyannjones/cicd:latest bash

# Execute the training pipeline
docker exec modelv1 python prediction_model/training_pipeline.py

# Execute pytest
docker exec modelv1 pytest -v --junitxml TestResults.xml --cache-clear

# If you want to visualize TestResults.xml
docker cp modelv1:/code/src/TestResults.xml .

# Run the FastAPI application
docker exec -d -w /code modelv1 python main.py

# Copy a specific file from localhost to docker container
docker cp main.py bb0fc9f02937b1b36e18a39f1729671c8c1820fddb1aaf659aecc5030fc037fb:/main.py

```

# Jenkins Commands

```
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```
