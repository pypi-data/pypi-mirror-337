import shutil
import subprocess
import sys

OLLAMA_INSTALL_URL = "https://ollama.com/download"
OLLAMA_LINUX_INSTALL_URL = "https://ollama.com/install.sh"

def is_ollama_installed():
    """Check if Ollama is installed."""
    return shutil.which("ollama") is not None


def install_ollama():
    """Install Ollama based on the machine type."""
    if sys.platform == "darwin":  # macOS
        print("Installing Ollama on macOS...")
        subprocess.run(
            ["brew", "install", "--cask", "ollama"], check=True
        )
    elif sys.platform.startswith("linux"):
        print("Installing Ollama on Linux...")
        subprocess.run(
            ["bash", "-c", f"curl -fsSL {OLLAMA_LINUX_INSTALL_URL} | bash"], check=True
        )
    else:
        print("Unsupported platform for automated installation. Please install Ollama manually from:", OLLAMA_INSTALL_URL)
        sys.exit(1)


def pull_model(model_name="mistral"):
    """Download a model using Ollama if not already available."""
    if not is_ollama_installed():
        install_ollama()

    print(f"Checking if model '{model_name}' is available...")
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        print(f"Model '{model_name}' is ready!")
    except subprocess.CalledProcessError:
        print(f"Failed to download model '{model_name}'. Check Ollama installation.")


def ensure_ollama_setup(model_name="mistral"):
    """Ensure Ollama and the required model are set up."""
    if not is_ollama_installed():
        install_ollama()
    else:
        print("Ollama is already installed.")
    pull_model(model_name)
