import sys

from kubernetes import client
from kubernetes import config
from kubernetes.client.rest import ApiException

arguments = sys.argv

# Delete first argument (script name)
del arguments[0]

valid_arguments = [
    'namespace',
    'cronjob-name',
]

arguments_dict = {}

for argument in arguments:
    argument_name, argument_value = argument.split('=')
    arguments_dict[argument_name] = argument_value

namespace = arguments_dict['namespace']
cronjob_name = arguments_dict['cronjob-name']

config.load_incluster_config()
k8s_batch_client = client.BatchV1Api()

# corp-datascience-dev-pre
try:
    api_response = k8s_batch_client.list_namespaced_job(namespace)
    for job in api_response.items:
        status = job.status
        job_name = job.metadata.labels['job-name']

        if (
            status.failed or
            status.succeeded and cronjob_name in job_name
        ):
            k8s_batch_client.delete_namespaced_job(
                name=job_name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy='Foreground',
                )
            )

except ApiException as e:
    print("Exception when calling BatchV1Api->list_namespaced_job: %s\n" % e)
