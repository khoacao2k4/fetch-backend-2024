# Fetch Batchend Coding Exercise

## Requirements

- `Python 3.9+`
- `pip` (Python package installer)
- `bash` for running the test script

## Setup Steps
### Setting Up the Virtual Environment
1. Create a virtual environment and activate:

Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### Installing Dependencies
With the virtual environment activated, install the required dependencies using the provided requirements.txt file:
```bash
pip install -r requirements.txt
```
### Running the backend server
Start the Flask server, which will run on http://127.0.0.1:8000 by default:
```bash
python3 main.py
```
4. Testing the API

- **Using curl**: Test the API endpoints using curl commands:

    + Add Points:
    ```bash
    curl -X POST http://127.0.0.1:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}'
    ```

    + Spend Points:
    ```bash
    curl -X POST http://127.0.0.1:8000/spend -H "Content-Type: application/json" -d '{"points": 5000}'
    ```

    + Get Balance:
    ```bash
    curl -X GET http://127.0.0.1:8000/balance
    ```

- **Using the Test Script**: Alternatively, you can run the included bash script to test all API endpoints:

    ```bash
    chmod +x ./test_sol.sh
    ./test_sol.sh
    ```

### Cleanup
When finished, deactivate the virtual environment and stop the server process.
```bash
deactivate
```

### Notes
When run for the first time, a `SQLite` database will be created and be put into folder `instance`, which will persistent (keep the same records as before) when run the server later times. To reset, just remove the folder! 

```bash
rm -r instance
```