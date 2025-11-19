# Image → Story Generator  
Flask app with **PostgreSQL**, **Docker Compose**, and **Ollama**

This project allows a user to upload an image, send it to a local Ollama model, and receive a generated story.  
Each story is stored in a PostgreSQL database, using the image filename as an identifier.  
If the same image is uploaded again, the app returns the previously saved story instead of generating a new one.

---

## 🚀 Features
- Upload an image through the Flask API  
- Generate a story from the image using an Ollama model  
- Save stories in PostgreSQL (image name = identifier)  
- Return existing story if the image was already processed  
- Fully containerized using **Docker Compose**  
- Ability to map a **local Ollama model** into the container so you don’t have to re-pull it every time

---

## 📦 Project Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. 🧠 Setting Up Ollama (Linux)

To avoid pulling the model every time the container is rebuilt, we will map the local Ollama model directory into the Docker container.

1. Install Ollama according to the official instructions:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
2. Start the Ollama server
    ```bash
    ollama serve
    ```
3. In another terminal, pull the model you want to use:
    ```bash
    ollama pull llava-llama3
    ```
    Make sure the pulled model name matches the model used inside your Flask app.

### 3. 🔍 Finding the Model Directory (Host & Container)
1. On your host machine:
    ```bash
    sudo find / -name models | grep "ollama"
    ```
    This typically outputs something like:
    ```bash
    /usr/share/ollama/models
    /home/<user>/.ollama/models
    ```
    Use the directory that contains your pulled model(s).
2. You need to know the location of the model path inside the container to map it correctly.
    Start the container once:
    ```bash
    docker compose up --build
    ```
    In another terminal, find the container ID:
    ```bash
    docker ps
    ```
    And open a shell inside the container:
    ```bash
    docker exec -it <container_id> /bin/bash
    ```
    Find the internal model directory:
    ```bash
    find / -name models | grep "ollama"
    ```
    This will get you a path such as:
    ```bash
    /root/.ollama/models
    ```

### 4. 🔗 Mapping the Model Volume
In your `docker-compose.yml`, map the local models folder into the container:
```bash
volumes:
  - /path/to/local/ollama/models:/root/.ollama/models
``` 

This ensures:
- The container uses your local model files
- You do not need to pull large models again when rebuilding the container
- The model remains persistent across rebuilds

### 5. ▶️ Run the Full Stack
```bash
docker compose up --build
``` 

## TODOs

- Clean up the code: add docstrings and types
- Move hyperparameters into a config file?

