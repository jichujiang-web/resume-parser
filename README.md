# Project Setup Guide

## Overview
This project provides a containerized environment for running a local model-based chatbot using **Llama 3.2 1B Instruct GGUF**.

You can either:
1. **Download a prebuilt Docker container**, or  
2. **Build your own container** after downloading the model.

---

## Option 1: Download the Prebuilt Container

Download the `.tar` file containing the prebuilt Docker image.  
This file already includes all dependencies and the **GGUF model**, so you **do not need any other files**.

To load and run the container:

```bash
docker load -i your_container_image.tar
docker run -it -p 8080:8080 your_container_name
```

---

## Option 2: Build the Container Yourself

If you prefer to build the container manually, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Download the model file
Download the GGUF model from the following link:

👉 [Llama-3.2-1B-Instruct-f16.gguf](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/blob/main/Llama-3.2-1B-Instruct-f16.gguf)

Then place it into the `models/` folder in your project directory.

### 3. Build and run the container
```bash
docker build -t my-chatbot .
docker run -it -p 8080:8080 my-chatbot
```

---

## Navigating the User Interface

Below are visual guides to help you navigate the UI:

### Main Dashboard
![Main Dashboard](images/ui_dashboard.png)

### Model Interaction Screen
![Model Interaction](images/ui_model_interaction.png)

### Settings Panel
![Settings Panel](images/ui_settings.png)

---

## Troubleshooting

- Ensure the `models` folder contains the `.gguf` file before building.
- If the container fails to load, check that Docker has sufficient memory.
- Ports 8080–8090 should be available before running the container.

---

## License
This project is distributed under the MIT License.
