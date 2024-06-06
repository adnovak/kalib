# kalib

calibration app

## Installation & Usage

Clone repository and inside of it execute commands bellow. Instruction may slightly change according to your operating 
system.

### Using conda

```shell

# Will create a new conda environment called kalib and install requirements
conda create --name kalib --file requirements.txt

# Activate created environment
conda activate kalib

# Execute application
python -m kaliberx
```

### Using pip

```shell
# Create virtual environment
python -m venv .env

source .env/bin/activate # Linux/macOS
.\.venv\Scripts\activate.bat # Windows CMD
.\.venv\Scripts\activate.ps1 # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Execute application
python -m kaliberx
```


