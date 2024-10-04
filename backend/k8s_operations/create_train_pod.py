from kubernetes import client, config

url = "http://127.0.0.1:8000/trained_model/"

def create_train_pod(train_name: str, start_day: str, end_day: str, cpu: str = "1000m", mem: str = "1Gi"):
    config.load_kube_config()
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="train-job-" + train_name.lower()),
        spec=client.V1JobSpec(
            ttl_seconds_after_finished=30,
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(name="trainer-" + train_name.lower()),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="trainer-container",
                            image="konglsh96/rain-forecast-mlops:trainer",
                            command=["python3", "train_main.py"],
                            args=["--url", url, "--train_name", train_name.lower(), "--start_day", start_day, "--end_day",
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
