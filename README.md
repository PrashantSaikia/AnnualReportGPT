# AnnualReportGPT
Q&amp;A on 10-K Reports

https://2ed04bed0ff711d80b.gradio.live

# Usage
```
git clone https://github.com/PrashantSaikia/AnnualReportGPT.git
pip install -r requirements.txt
python run app.py
```

# Steps for Kubernetes Deployment in GCP

Source: https://cloud.google.com/build/docs/build-push-docker-image

**Create a Docker repository in Artifact Registry**
Create a new Docker repository named quickstart-docker-repo in the location us-west2 with the description "Docker repository":

```
gcloud artifacts repositories create quickstart-docker-repo --repository-format=docker \
    --location=us-west2 --description="Docker repository"
```

Verify that your repository was created:

```
gcloud artifacts repositories list
You will see quickstart-docker-repo in the list of displayed repositories.
```

**Build an image using Dockerfile**
Cloud Build allows you to build a Docker image using a Dockerfile. You don't require a separate Cloud Build config file.

To build using a Dockerfile:

Get your Google Cloud project ID by running the following command:

```
gcloud config get-value project
```

Run the following command from the directory containing quickstart.sh and Dockerfile:

```
gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/project-id/quickstart-docker-repo/quickstart-image:tag1
Note: If your project ID contains a colon, replace the colon with a forward slash.
After the build is complete, you will see an output similar to the following:
```
```
DONE
------------------------------------------------------------------------------------------------------------------------------------
ID                                    CREATE_TIME                DURATION  SOURCE   IMAGES     STATUS
545cb89c-f7a4-4652-8f63-579ac974be2e  2020-11-05T18:16:04+00:00  16S       gs://gcb-docs-project_cloudbuild/source/1604600163.528729-b70741b0f2d0449d8635aa22893258fe.tgz  us-west2-docker.pkg.dev/gcb-docs-project/quickstart-docker-repo/quickstart-image:tag1  SUCCESS
You've just built a Docker image named quickstart-image using a Dockerfile and pushed the image to Artifact Registry.
```

**Build an image using a build config file**
In this section you will use a Cloud Build config file to build the same Docker image as above. The build config file instructs Cloud Build to perform tasks based on your specifications.

In the same directory that contains quickstart.sh and the Dockerfile, create a file named cloudbuild.yaml with the following contents. This file is your build config file. At build time, Cloud Build automatically replaces $PROJECT_ID with your project ID.

```
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: [ 'build', '-t', 'us-west2-docker.pkg.dev/$PROJECT_ID/quickstart-docker-repo/quickstart-image:tag1', '.' ]
images:
- 'us-west2-docker.pkg.dev/$PROJECT_ID/quickstart-docker-repo/quickstart-image:tag1'
```

Start the build by running the following command:

```
gcloud builds submit --region=us-west2 --config cloudbuild.yaml
```

When the build is complete, you will see an output similar to the following:

```
DONE
------------------------------------------------------------------------------------------------------------------------------------
ID                                    CREATE_TIME                DURATION  SOURCE          IMAGES          STATUS
046ddd31-3670-4771-9336-8919e7098b11  2020-11-05T18:24:02+00:00  15S       gs://gcb-docs-project_cloudbuild/source/1604600641.576884-8153be22c94d438aa86c78abf11403eb.tgz  us-west2-docker.pkg.dev/gcb-docs-project/quickstart-docker-repo/quickstart-image:tag1  SUCCESS
You've just built quickstart-image using the build config file and pushed the image to Artifact Registry.
```

After this, create a Kubernetes cluster in automated mode, give the docker image ID from above, and deploy the cluster. Wait for a few minutes for the cluster to get ready, could be a couple of hours sometimes depending on the location and the traffic, and it should run fine.
