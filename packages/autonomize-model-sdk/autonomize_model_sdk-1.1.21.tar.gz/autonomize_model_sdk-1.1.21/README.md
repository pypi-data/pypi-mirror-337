# ModelHub SDK

ModelHub SDK is a powerful tool for orchestrating and managing machine learning workflows, experiments, datasets, and deployments on Kubernetes. It integrates seamlessly with MLflow and supports custom pipelines, dataset management, model logging, and serving through Kserve.

![Python Version](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![PyPI Version](https://img.shields.io/pypi/v/autonomize-model-sdk?style=for-the-badge&logo=pypi)
![Code Formatter](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)
![Code Linter](https://img.shields.io/badge/linting-pylint-green.svg?style=for-the-badge)
![Code Checker](https://img.shields.io/badge/mypy-checked-blue?style=for-the-badge)
![Code Coverage](https://img.shields.io/badge/coverage-96%25-a4a523?style=for-the-badge&logo=codecov)

## Table of Contents

- [ModelHub SDK](#modelhub-sdk)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
  - [CLI Tool](#cli-tool)
  - [Quickstart](#quickstart)
  - [Experiments and Runs](#experiments-and-runs)
    - [Logging Parameters and Metrics](#logging-parameters-and-metrics)
    - [Artifact Management](#artifact-management)
  - [Pipeline Management](#pipeline-management)
    - [Basic Pipeline](#basic-pipeline)
    - [Running a Pipeline](#running-a-pipeline)
    - [Advanced Configuration](#advanced-configuration)
  - [Dataset Management](#dataset-management)
    - [Loading Datasets](#loading-datasets)
    - [Using Blob Storage for Dataset](#using-blob-storage-for-dataset)
  - [Model Deployment through KServe](#model-deployment-through-kserve)
    - [Create a model wrapper:](#create-a-model-wrapper)
    - [Serve models with ModelHub:](#serve-models-with-modelhub)
    - [Deploy with KServe:](#deploy-with-kserve)
  - [Examples](#examples)
    - [Training Pipeline with Multiple Stages](#training-pipeline-with-multiple-stages)
    - [Dataset Version Management](#dataset-version-management)
- [InferenceClient](#inferenceclient)
  - [Installation](#installation-1)
  - [Authentication](#authentication)
  - [Text Inference](#text-inference)
  - [File Inference](#file-inference)
    - [Local File Path](#local-file-path)
    - [File Object](#file-object)
    - [URL](#url)
    - [Signed URL from Cloud Storage](#signed-url-from-cloud-storage)
  - [Response Format](#response-format)
  - [Error Handling](#error-handling)
  - [Additional Features](#additional-features)
- [PromptClient](#promptclient)
  - [Installation](#installation-2)
  - [Authentication](#authentication-1)
  - [Create Prompt](#create-prompt)
  - [Add Prompt Version](#add-prompt-version)
  - [Get All Prompts](#get-all-prompts)
  - [Get All Prompt Versions](#get-all-prompt-versions)
  - [Get Specific Prompt Versions](#get-specific-prompt-versions)
  - [Get Prompt By ID](#get-prompt-by-id)
  - [Get Prompt By Name](#get-prompt-by-name)
  - [Update Prompt Info](#update-prompt-info)
  - [Update Specific Prompt Version](#update-specific-prompt-version)
  - [Delete A Prompt Version](#delete-a-prompt-version)
  - [Delete Prompt](#delete-prompt)
  - [Feedback \& Contributions](#feedback--contributions)
  - [License](#license)
- [ML Monitoring](#model-monitoring-and-evaluation)
  - [LLL](#llm-monitoring)
  - [Traditional Model Monitoring](#traditional-ml-monitoring)

## Installation

To install the ModelHub SDK, simply run:

```bash
pip install autonomize-model-sdk
```

## Environment Setup

Ensure you have the following environment variables set in your system:

```bash
export MODELHUB_BASE_URL=https://api-modelhub.example.com
export MODELHUB_CLIENT_ID=your_client_id
export MODELHUB_CLIENT_SECRET=your_client_secret
export MLFLOW_EXPERIMENT_ID=your_experiment_id
```

Alternatively, create a .env file in your project directory and add the above environment variables.

## CLI Tool

The ModelHub SDK includes a command-line interface for managing ML pipelines:

```bash
# Start a pipeline in local mode (with local scripts)
pipeline start -f pipeline.yaml --mode local --pyproject pyproject.toml

# Start a pipeline in CI/CD mode (using container)
pipeline start -f pipeline.yaml --mode cicd
```

CLI Options:

- `-f, --file`: Path to pipeline YAML file (default: pipeline.yaml)
- `--mode`: Execution mode ('local' or 'cicd')
  - local: Runs with local scripts and installs dependencies using Poetry
  - cicd: Uses container image with pre-installed dependencies
- `--pyproject`: Path to pyproject.toml file (required for local mode)

## Quickstart

The ModelHub SDK allows you to easily log experiments, manage pipelines, and use datasets.

Here's a quick example of how to initialize the client and log a run:

```python
import os
from modelhub.clients import MLflowClient

# Initialize the ModelHub client
client = MLflowClient(base_url=os.getenv("MODELHUB_BASE_URL"))
experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID")

client.set_experiment(experiment_id=experiment_id)

# Start an MLflow run
with client.start_run(run_name="my_experiment_run"):
    client.mlflow.log_param("param1", "value1")
    client.mlflow.log_metric("accuracy", 0.85)
    client.mlflow.log_artifact("model.pkl")
```

## Experiments and Runs

ModelHub SDK provides an easy way to interact with MLflow for managing experiments and runs.

### Logging Parameters and Metrics

To log parameters, metrics, and artifacts:

```python
with client.start_run(run_name="my_run"):
    # Log parameters
    client.mlflow.log_param("learning_rate", 0.01)

    # Log metrics
    client.mlflow.log_metric("accuracy", 0.92)
    client.mlflow.log_metric("precision", 0.88)

    # Log artifacts
    client.mlflow.log_artifact("/path/to/model.pkl")
```

### Artifact Management

You can log or download artifacts with ease:

```python
# Log artifact
client.mlflow.log_artifact("/path/to/file.csv")

# Download artifact
client.mlflow.artifacts.download_artifacts(run_id="run_id_here", artifact_path="artifact.csv", dst_path="/tmp")
```

## Pipeline Management

ModelHub SDK enables users to define, manage, and run multi-stage pipelines that automate your machine learning workflow. You can define pipelines in YAML and submit them using the SDK.

### Basic Pipeline

Here's a simple pipeline example:

```yaml
name: "Simple Pipeline"
description: "Basic ML pipeline"
experiment_id: "123"
image_tag: "my-image:1.0.0"
stages:
  - name: train
    type: custom
    script: scripts/train.py
```

### Running a Pipeline

Using CLI:

```bash
# Local development
pipeline start -f pipeline.yaml --mode local --pyproject pyproject.toml

# CI/CD environment
pipeline start -f pipeline.yaml --mode cicd
```

Using SDK:

```python
from modelhub.clients import PipelineManager

pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")
```

### Advanced Configuration

For detailed information about pipeline configuration including:

- Resource management (CPU, Memory, GPU)
- Node scheduling with selectors and tolerations
- Blob storage integration
- Stage dependencies
- Advanced examples and best practices

See our [Pipeline Configuration Guide](./PIPELINE.md).

## Dataset Management

ModelHub SDK allows you to load and manage datasets easily, with support for loading data from external storage or datasets managed through the frontend.

### Loading Datasets

To load datasets using the SDK:

```python
from modelhub import load_dataset

# Load a dataset by name
dataset = load_dataset("my_dataset")

# Load a dataset from a specific directory
dataset = load_dataset("my_dataset", directory="data_folder/")

# Load a specific version and split
dataset = load_dataset("my_dataset", version=2, split="train")

```

### Using Blob Storage for Dataset

```python
# Load dataset from blob storage
dataset = load_dataset(
    "my_dataset",
    blob_storage_config={
        "container": "data",
        "blob_url": "https://storage.blob.core.windows.net",
        "mount_path": "/data"
    }
)

```

## Model Deployment through KServe

Deploy models via KServe after logging them with MLflow:

### Create a model wrapper:

Use the MLflow PythonModel interface to define your model's prediction logic.

```python
import mlflow.pyfunc
import joblib

class ModelWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load("/path/to/model.pkl")

    def predict(self, context, model_input):
        return self.model.predict(model_input)

# Log the model
client.mlflow.pyfunc.log_model(
    artifact_path="model",
    python_model=ModelWrapper()
)
```

### Serve models with ModelHub:

ModelHub SDK provides classes for serving models through KServe:

```python
from modelhub.serving import ModelhubModelService, ModelServer

# Create model service
model_service = ModelhubModelService(
    name="my-classifier",
    run_uri="runs:/abc123def456/model",
    model_type="pyfunc"
)

# Load the model
model_service.load()

# Start the server
ModelServer().start([model_service])
```

ModelHub supports multiple model types including text, tabular data, and image processing. For comprehensive documentation on model serving capabilities, see our [Model Serving Guide](./SERVING.md).

### Deploy with KServe:

After logging the model, deploy it using KServe:

```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "model-service"
  namespace: "modelhub"
  labels:
    azure.workload.identity/use: "true"
spec:
  predictor:
    containers:
      - image: your-registry.io/model-serve:latest
        name: model-service
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        command:
          [
            "sh",
            "-c",
            "python app/main.py --model_name my-classifier --run runs:/abc123def456/model",
          ]
        env:
          - name: MODELHUB_BASE_URL
            value: "https://api-modelhub.example.com"
    serviceAccountName: "service-account-name"
```

## Examples

### Training Pipeline with Multiple Stages

```python
from modelhub.clients import MLflowClient, PipelineManager

# Setup clients
mlflow_client = MLflowClient()
pipeline_manager = PipelineManager()

# Define and run pipeline
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")

# Track experiment in MLflow
with mlflow_client.start_run(run_name="Training Run"):
    # Log training parameters
    mlflow_client.log_param("model_type", "transformer")
    mlflow_client.log_param("epochs", 10)

    # Log metrics
    mlflow_client.log_metric("train_loss", 0.123)
    mlflow_client.log_metric("val_accuracy", 0.945)

    # Log model artifacts
    mlflow_client.log_artifact("model.pkl")

```

### Dataset Version Management

```python
from modelhub.clients import DatasetClient

# Initialize client
dataset_client = DatasetClient()

# List available datasets
datasets = dataset_client.list_datasets()

# Get specific version
dataset_v2 = dataset_client.get_dataset_versions("dataset_id")

# Load dataset with version control
dataset = dataset_client.load_dataset(
    "my_dataset",
    version=2,
    split="train"
)

```

# InferenceClient

The `InferenceClient` provides a simple interface to perform inference using deployed models. It supports both text-based and file-based inference with comprehensive error handling and support for various input types.

## Installation

The inference client is part of the ModelHub SDK optional dependencies. To install:

```bash
pip install autonomize-model-sdk[inference]
```

Or with Poetry:

```bash
poetry add autonomize-model-sdk --extras inference
```

## Authentication

The client supports multiple authentication methods:

```python
from modelhub.clients import InferenceClient

# Using environment variables (MODELHUB_BASE_URL, MODELHUB_CLIENT_ID, MODELHUB_CLIENT_SECRET)
client = InferenceClient()

# Using direct parameters
client = InferenceClient(
    base_url="https://your-modelhub-instance",
    sa_client_id="your-client-id",
    sa_client_secret="your-client-secret",
    genesis_client_id="client id",
    genesis_copilot_id="copilot id"
)

# Using a token
client = InferenceClient(
    base_url="https://your-modelhub-instance",
    token="your-token"
)
```

## Text Inference

For models that accept text input:

```python
# Simple text inference
response = client.run_text_inference(
    model_name="text-model",
    text="This is the input text"
)

# With additional parameters
response = client.run_text_inference(
    model_name="llm-model",
    text="Translate this to French: Hello, world!",
    parameters={
        "temperature": 0.7,
        "max_tokens": 100
    }
)

# Access the result
result = response["result"]
print(f"Processing time: {response.get('processing_time')} seconds")
```

## File Inference

The client supports multiple file input methods:

### Local File Path

```python
# Using a local file path
response = client.run_file_inference(
    model_name="image-recognition",
    file_path="/path/to/image.jpg"
)
```

### File Object

```python
# Using a file-like object
with open("document.pdf", "rb") as f:
    response = client.run_file_inference(
        model_name="document-processor",
        file_path=f,
        file_name="document.pdf",
        content_type="application/pdf"
    )
```

### URL

```python
# Using a URL
response = client.run_file_inference(
    model_name="image-recognition",
    file_path="https://example.com/images/sample.jpg"
)
```

### Signed URL from Cloud Storage

```python
# Using a signed URL from S3 or Azure Blob Storage
response = client.run_file_inference(
    model_name="document-processor",
    file_path="https://your-bucket.s3.amazonaws.com/path/to/document.pdf?signature=...",
    file_name="confidential-document.pdf",  # Optional: Override filename
    content_type="application/pdf"          # Optional: Override content type
)
```

## Response Format

The response format is consistent across inference types:

```python
{
    "result": {
        # Model-specific output
        # For example, text models might return:
        "text": "Generated text",

        # Image models might return:
        "objects": [
            {"class": "car", "confidence": 0.95, "bbox": [10, 20, 100, 200]},
            {"class": "person", "confidence": 0.87, "bbox": [150, 30, 220, 280]}
        ]
    },
    "processing_time": 0.234,  # Time in seconds
    "model_version": "1.0.0",  # Optional version info
    "metadata": {              # Optional additional information
        "runtime": "cpu",
        "batch_size": 1
    }
}
```

## Error Handling

The client provides comprehensive error handling:

```python
from modelhub.clients import InferenceClient
from modelhub.core import ModelHubException

client = InferenceClient()

try:
    response = client.run_text_inference("model-name", "input text")
    print(response)
except ModelHubException as e:
    print(f"Inference failed: {e}")
    # Handle the error
```

## Additional Features

- **Automatic content type detection**: The client automatically detects the content type of files based on their extension
- **Customizable timeout**: You can set a custom timeout for inference requests
- **Comprehensive logging**: All operations are logged for easier debugging

For more detailed information, refer to the API documentation or the example scripts.

# PromptClient

The `PromptClient` provides an interface for managing prompts, including creating, updating, deleting, and retrieving prompts and their versions.

## Installation

The prompt client is included as part of the ModelHub SDK. To install it:

```bash
pip install autonomize-model-sdk[prompt]
```

Or with Poetry:

```bash
poetry add autonomize-model-sdk --extras prompt
```

## Authentication

The client supports multiple authentication methods:

```python
from modelhub.clients.prompt_client import PromptClient

# Using environment variables (MODELHUB_BASE_URL, MODELHUB_CLIENT_ID, MODELHUB_CLIENT_SECRET)
client = PromptClient()

# Using direct parameters
client = PromptClient(
    base_url="https://your-modelhub-instance",
    sa_client_id="your-client-id",
    sa_client_secret="your-client-secret",
    genesis_client_id="client id",
    genesis_copilot_id="copilot id"
)

# Using a token
client = PromptClient(
    base_url="https://your-modelhub-instance",
    token="your-token"
)
```

## Create Prompt

Create a new prompt and store it in the database:

```python
response = client.create_prompt(
    name="summarization",
    description="Summarizes long-form text into a concise summary.",
    template="Summarize this text {context}",
    prompt_type="USER"
)
print(f"Created prompt: {response}")
```

## Add Prompt Version

Add a new version to an existing prompt:

```python
response = client.add_prompt_version(
    template="Summarize this text:{context}"
)
print(f"added prompt version: {response}")
```

## Get All Prompts

Get List of All prompts

```python
prompts = client.get_prompts()
print(prompts)
```

## Get All Prompt Versions

Retrieve all versions of a specific prompt. If no prompt name is provided, returns versions for all prompts.

```python
prompt_versions = client.get_prompt_versions(prompt_name=prompt_name)
print(prompts_versions)
```

## Get Specific Prompt Versions

Retrieves a specific prompt version. If no version is provided, returns latest version.

```python
prompt_version = client.get_prompt_version(prompt_name=prompt_name,version=version)
print( prompt_version)
```

## Get Prompt By ID

Retrieves a specific prompt By its ID.

```python
prompt = await client.get_prompt(prompt_id=prompt_id)
print(f'prompt with {prompt_id}: ',prompt)
```

## Get Prompt By Name

Retrieves a specific prompt By its Name.

```python
prompt = await client.get_prompt_by_name(name=prompt_name)
print(f'prompt with name {prompt_name}: ',prompt)
```

## Update Prompt Info

Updates prompt details such as name, description, or prompt type.

```python
updated_prompt = await client.update_prompt(prompt_id=prompt_id,prompt={"description": "updated description"})
print(f'updated prompt with {prompt_id}: ',updated_prompt)
```

## Update Specific Prompt Version

Updates a specific prompt version, primarily the template.

```python
update_prompt_version = await client.update_prompt_version(prompt_name=prompt_name,version=version,update_prompt_version={"template": "updated prompt template"})
print(f'updated prompt version {version} of {prompt_name}: ',update_prompt_version)
```

## Delete A Prompt Version

Deletes a specific prompt version.

```python
deleted_prompt_version = await client.delete_prompt_version(prompt_id=prompt_id,version=version)
print(f'deleted prompt version {version} of prompt with id {prompt_id}')
```

## Delete Prompt

Deletes a specific prompt with all its versions.

```python
deleted_prompt = await client.delete_prompt(prompt_id=prompt_id)
print(f'deleted prompt with {prompt_id}')
```

# Model Monitoring and Evaluation

ModelHub SDK provides comprehensive tools for monitoring and evaluating both traditional ML models and Large Language Models (LLMs). These tools help track model performance, detect data drift, and assess LLM-specific metrics.

## LLM Monitoring

The `LLMMonitor` utility allows you to evaluate and monitor LLM outputs using specialized metrics and visualizations.

### Basic LLM Evaluation

```python
from modelhub.monitors.llm_monitor import LLMMonitor
from modelhub.clients.mlflow_client import MLflowClient

# Initialize clients
mlflow_client = MLflowClient()
llm_monitor = LLMMonitor(mlflow_client=mlflow_client)

# Create a dataframe with LLM responses
data = pd.DataFrame({
    "prompt": ["Explain AI", "What is MLOps?"],
    "response": ["AI is a field of computer science...", "MLOps combines ML and DevOps..."],
    "category": ["education", "technical"]
})

# Create column mapping
column_mapping = llm_monitor.create_column_mapping(
    prompt_col="prompt",
    response_col="response",
    categorical_cols=["category"]
)

# Run evaluations
length_report = llm_monitor.evaluate_text_length(
    data=data,
    response_col="response",
    column_mapping=column_mapping,
    save_html=True
)

# Generate visualizations
dashboard_path = llm_monitor.generate_dashboard(
    data=data,
    response_col="response",
    category_col="category"
)

# Log metrics to MLflow
llm_monitor.log_metrics_to_mlflow(length_report)
```

### Evaluating Content Patterns

```python
patterns_report = llm_monitor.evaluate_content_patterns(
    data=data,
    response_col="response",
    words_to_check=["AI", "model", "learning"],
    patterns_to_check=["neural network", "deep learning"],
    prefix_to_check="I'll explain"
)
```

### Semantic Properties Analysis

```python
semantic_report = llm_monitor.evaluate_semantic_properties(
    data=data,
    response_col="response",
    prompt_col="prompt",
    check_sentiment=True,
    check_toxicity=True,
    check_prompt_relevance=True
)
```

### Comprehensive Evaluation

```python
results = llm_monitor.run_comprehensive_evaluation(
    data=data,
    response_col="response",
    prompt_col="prompt",
    categorical_cols=["category"],
    words_to_check=["AI", "model", "learning"],
    run_sentiment=True,
    run_toxicity=True,
    save_html=True
)
```

### LLM-as-Judge Evaluation

Evaluate responses using OpenAI's models as a judge (requires OpenAI API key):

```python
judge_report = llm_monitor.evaluate_llm_as_judge(
    data=data,
    response_col="response",
    check_pii=True,
    check_decline=True,
    custom_evals=[{
        "name": "Educational Value",
        "criteria": "Evaluate whether the response has educational value.",
        "target": "educational",
        "non_target": "not_educational"
    }]
)
```

### Comparing LLM Models

Compare responses from different LLM models:

```python
comparison_report = llm_monitor.generate_comparison_report(
    reference_data=model_a_data,
    current_data=model_b_data,
    response_col="response",
    category_col="category"
)

comparison_viz = llm_monitor.create_comparison_visualization(
    reference_data=model_a_data,
    current_data=model_b_data,
    response_col="response",
    metrics=["length", "word_count", "sentiment_score"]
)
```

## Traditional ML Monitoring

The SDK also includes `MLMonitor` for traditional ML models, providing capabilities for:

- Data drift detection
- Data quality assessment
- Model performance monitoring
- Target drift analysis
- Regression and classification metrics

```python
from modelhub.monitors.ml_monitor import MLMonitor

ml_monitor = MLMonitor(mlflow_client=mlflow_client)

results = ml_monitor.run_and_log_reports(
    reference_data=reference_data,
    current_data=current_data,
    report_types=["data_drift", "data_quality", "target_drift", "regression"],
    column_mapping=column_mapping,
    target_column="target",
    prediction_column="prediction",
    log_to_mlflow=True
)
```

## Architecture

ModelHub SDK uses a modular architecture:

- **Interface Layer**: Abstract interfaces defining monitoring functionality (`LLMMonitorInterface`, `ModelMonitorInterface`)
- **Implementation Layer**: Implementations of monitoring interfaces (`EvidentlyLLMMonitor`, `EvidentlyModelMonitor`)
- **Facade Layer**: Easy-to-use facades that provide unified access to monitoring functionality (`LLMMonitor`, `MLMonitor`)
- **Factory**: Factories for creating monitor instances based on specified providers

## Advanced Usage

To share functionality between ML and LLM monitors:

```python
# Create ML monitor
ml_monitor = MLMonitor(mlflow_client=mlflow_client)

# Create LLM monitor that shares functionality with ML monitor
llm_monitor = LLMMonitor(mlflow_client=mlflow_client, ml_monitor=ml_monitor)
```

Check out the `examples/evaluations` directory for complete examples of both LLM and traditional ML monitoring.

## Feedback & Contributions

We welcome contributions to the ModelHub SDK! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows our style guidelines and includes appropriate tests.

For feedback or support:

- Open an issue on GitHub
- Contact the ModelHub team directly
- Check our documentation for updates

## License

Copyright (C) Autonomize AI - All Rights Reserved

The contents of this repository cannot be copied and/or distributed without the explicit permission from Autonomize.ai

```

```
