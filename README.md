# Data Engineering Project

This project combines and cleans crime records from a JSON file and district details from a scanned PDF using OCR. The processed data is  stored in a PostgreSQL database (deployed via Docker). A Streamlit dashboard is provided to visualize key crime metrics.

**Note:** This project has been containerized for consistent deployment. The dashboard component can be run locally with Streamlit.

## Setup & Installation

1. **Clone the Repository:**  
   Clone or download the project files into a local directory.

2. **Install Dependencies:**  
   In the project root, run:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   brew install tesseract
   docker-compose up -d
   ```

3. **Run the code:**
    ```bash
    python main.py
    docker build -t crime-pipeline .
    docker run --rm crime-pipeline
    ```
4. **Running the streamlit dashboard locally:**
    ```bash
    streamlit run dashboard.py
    ```
    open http://localhost:8501/





