---
title: Musheff Api
emoji: 🍄
colorFrom: yellow
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: Mushrooms Classification API
app-port: 7860
datasets:
  - SoFa325/12_popular_russia_mushrooms_edible_poisonous
models:
  - blasisd/musheff
---

# Musheff API - A Mushroom Classification REST API

**Identify edible and poisonous Russian mushrooms with AI-powered precision**

This project provides a production-ready REST API for classifying 12 common Russian mushroom species using computer vision. Built around the `musheff` fine-tuned EfficientNet-B3 model, it delivers vital safety insights by distinguishing between edible and poisonous varieties - potentially preventing dangerous misidentifications during foraging.

## Key Features

🍄 **Safety-first classification** - Critical edible/poisonous differentiation  
🧠 **State-of-the-art model** - Fine-tuned `EfficientNet-B3` architecture  
🌲 **Regional specialization** - Optimized for 12 common Russian species  
⚡️ **Production-ready** - Scalable REST API implementation  
🔍 **Transparent foundations** - Built on openly available datasets

## Technical Foundation

Powered by:

- Model: **[musheff](https://huggingface.co/blasisd/musheff)** (Custom fine-tuned EfficientNet-B3)
- Dataset: **[12_popular_russia_mushrooms_edible_poisonous](https://huggingface.co/datasets/SoFa325/12_popular_russia_mushrooms_edible_poisonous)**

## Getting Started

This guide provides step-by-step instructions to set up and run the project on your local machine for development and testing purposes. For details on deploying the project to a production environment, refer to the Deployment section.

### Prerequisites

To set up and run this project, ensure the following software and tools are installed on your system:

- **Python**: Version `3.10.12` or higher is required. Verify your Python version by running:

  ```bash
  python3 --version
  ```

- **Dependencies**: Install the required Python packages listed in requirements.txt using pip. Run the following command in your terminal:

  ```bash
  pip install -r requirements.txt
  ```

- **Docker (Optional)**: For containerized deployment. Install from [Docker's official site](https://docs.docker.com/get-docker/) and verify with:

  ```bash
  docker --version
  ```

### Local Development and Testing

To run the application locally for development and testing purposes, execute the following command in your terminal:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860 --reload
```

If it does not work, just try:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 7860 --reload
```

> [!WARNING]
> Ensure you are in the project's **src** directory before running the script or adapt running path (i.e. `python -m uvicorn src.main:app --host 0.0.0.0 --port 7860 --reload`).

## How to Use

The API exposes a classification endpoint at `/classify` that accepts mushroom images and returns:

- Predicted mushroom species
- Edibility status (edible/poisonous)
- Confidence score

### API Endpoint

`POST /classify`

### Request Format

```bash
curl -X POST "http://<your-api-url>/classify" \
  -H "Content-Type: multipart/form-data" \
  -F "image_file=@path/to/mushroom.jpg"
```

### Example Response

```bash
{
    "mushroom_type": "Pleurotus_ostreatus",
    "toxicity_profile": "edible",
    "confidence": 0.5491
}
```

## Deployment

### Deployment on Hugging Face Spaces

To deploy the project on Hugging Face Spaces, follow these steps:

1. Create an account on [Hugging Face](https://huggingface.co) if you don’t already have one.

2. Refer to the official [Spaces Overview](https://huggingface.co/docs/hub/en/spaces-overview) documentation for detailed instructions on setting up and deploying your project.

### Docker-based Deployment

#### Locally

- Build your docker image:

  ```bash
  docker build -t musheff-api .
  ```

- Run a container based on the image:

  ```bash
  docker run -it -p 7860:7860 musheff-api
  ```

#### On Hugging Face

1. Follow the official [Docker Spaces Guide](https://huggingface.co/docs/hub/en/spaces-sdks-docker-first-demo) for container setup.
2. Copy the available `Dockerfile` to your repository root or create your own.
3. Configure settings requirements in `README.md` metadata (especially app_port if you need a different port to use):

```yaml
---
title: Musheff Api
emoji: 🍄
colorFrom: yellow
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: Mushrooms Classification API
app-port: 7860
datasets:
  - SoFa325/12_popular_russia_mushrooms_edible_poisonous
models:
  - blasisd/musheff
---
```

### Deployment on Other Cloud Platforms

For deployment on other cloud or live systems, consult the documentation provided by your chosen service provider. Each platform may have specific requirements and steps for deploying Python-based applications.

## Built With

- [Python 3.10.12](http://www.python.org/) - Developing with the best programming language

## Authors

**Vlasios Dimitriadis** - _Initial work:_ [Musheff API](https://huggingface.co/spaces/blasisd/musheff-api)
````
