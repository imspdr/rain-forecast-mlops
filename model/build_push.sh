#!/bin/bash
sudo docker build -f Dockerfile.train -t konglsh96/rain-forecast-mlops:trainer .
sudo docker push konglsh96/rain-forecast-mlops:trainer

sudo docker build -f Dockerfile.serving -t konglsh96/rain-forecast-mlops:serving .
sudo docker push konglsh96/rain-forecast-mlops:serving