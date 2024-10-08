from kubernetes import client, config

#BACKEND_URL = "http://172.30.1.29:8000"
BACKEND_URL = "http://192.168.120.36:8000"

def create_train_pod(train_name: str, start_day: str, end_day: str, cpu: str = "1000m", mem: str = "1Gi"):
    config.load_kube_config()
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="train-job-" + train_name.lower()),
        spec=client.V1JobSpec(
            ttl_seconds_after_finished=10,
            backoff_limit=5,
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(name="trainer-" + train_name.lower()),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="trainer-container",
                            image="konglsh96/rain-forecast-mlops:trainer",
                            image_pull_policy="Always",
                            command=["python3", "train_main.py"],
                            args=["--url", BACKEND_URL, "--train_name", train_name.lower(), "--start_day", start_day, "--end_day",
                                  end_day],
                            resources=client.V1ResourceRequirements(
                                requests={"cpu": cpu, "memory": mem},
                                limits={"cpu": cpu, "memory": mem},
                            ),
                        )
                    ],
                    restart_policy="Never",
                ),
            )

        )
    )
    batch_v1 = client.BatchV1Api()
    batch_v1.create_namespaced_job(
        body=job,
        namespace="default"
    )

def create_trained_model_crd(model_name: str, storage_uri: str):
    config.load_kube_config()
    client.CustomObjectsApi().create_namespaced_custom_object(
        group="serving.kserve.io",
        version="v1alpha1",
        namespace="default",
        plural="trainedmodels",
        body={
            "apiVersion": "serving.kserve.io/v1alpha1",
            "kind": "TrainedModel",
            "metadata": {
                "name": model_name
            },
            "spec": {
                "model": {
                    "storageUri": storage_uri,
                    "framework": "custom",
                    "memory": "1Gi"
                },
                "inferenceService": "rain-multi-model"
            }
        }
    )

def delete_trained_model_crd(model_name: str):
    config.load_kube_config()
    client.CustomObjectsApi().delete_namespaced_custom_object(
        group="serving.kserve.io",
        version="v1alpha1",
        namespace="default",
        plural="trainedmodels",
        name=model_name
    )
