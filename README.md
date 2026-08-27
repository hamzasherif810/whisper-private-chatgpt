# whisper-private-chatgpt

Hi All,

This project is a **Multi-model private chatbot**. You can either clone it locally or deploy it on a cloud server.

I have deployed this code on a **g5.xlarge EC2 instance** (make sure that you have enough quota before initiating g5.xlarge).

I have used this AMI:
> **Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.13 (Ubuntu 26.04) 20260812**

because it comes with preinstalled Python3, Nvidia Driver (to run Ollama container using the Nvidia GPU), Docker, and Git.

## Setup Steps

After initiating and running the EC2, follow these steps:

### 1. Configure EC2 inbound rules

Allow requests on the following ports:

| Port | Purpose |
|------|---------|
| `27017` | Allow Streamlit to talk to MongoDB |
| `11434` | Allow Streamlit to talk to Ollama |
| `8501` | Allow users to access the Streamlit-based WhisperGPT website |

### 2. Install Python venv support

```bash
sudo apt install python3-venv
```

This will allow you to create a virtual environment and install the required dependencies in `requirements.txt`.

### 3. Install and run Ollama

Install the Ollama image from Docker, run the container using the GPU:

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Pull the required models:

```bash
docker exec -it ollama ollama pull llama3.1 gemma2:2b deepseek-r1
```

### 4. Install and run MongoDB

Install the MongoDB image from Docker and run it.

### 5. Clone the project repository

```bash
git clone <repository-url>
```

### 6. Navigate to the project directory

```bash
cd whisper-private-chatgpt
```

### 7. Configure environment variables

```bash
nano .env
```

Paste the content of the `.env template.txt` file and save it.

### 8. Create a virtual environment

```bash
python3 -m venv myenv
```

### 9. Activate the virtual environment

```bash
source myenv/bin/activate
```

### 10. Install dependencies

```bash
pip install -r requirements.txt
```

### 11. Run the application

```bash
streamlit run main.py
```
 
