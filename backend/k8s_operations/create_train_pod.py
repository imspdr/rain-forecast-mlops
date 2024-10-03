from kubernetes import client, config

url = "http://127.0.0.1:8000/trained_model/"

def create_train_pod(train_name: str, start_day: str, end_day: str, cpu: str = "1000m", mem: str = "1Gi"):
    config.load_kube_config()

    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name="trainer-" + train_name),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name="trainer-container",
                    image="konglsh96/rain-forecast-mlops:trainer",
                    command=["python3", "train_main.py"],
                    args=["--url", url, "--train_name", train_name, "--start_day", start_day, "--end_day", end_day],
                    resources=client.V1ResourceRequirements(
                        requests={"cpu": cpu, "memory": mem},
                        limits={"cpu": cpu, "memory": mem},
                    ),
                )
            ],
            restart_policy="Never",
            ttl_seconds_after_finished=30
        ),
    )

    api_instance = client.CoreV1Api()
    api_response = api_instance.create_namespaced_pod(
        namespace="default",
        body=pod
    )

    print(f"Pod created. Status: {api_response.status.phase}")
