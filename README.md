# sProGen - Automatic Sound Process Model Generation from Textual Description

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```sh
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run your project**:
    ```sh
    python Sample.py
    ```

### 2. Create a Setup Script

You can create a simple setup script to automate the creation of the virtual environment and installation of dependencies. Here’s an example `setup.sh` script:

```sh
#!/bin/bash

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete. Virtual environment created and dependencies installed."
