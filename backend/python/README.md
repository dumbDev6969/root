# Python Backend Project

## Description

This project is a Python-based backend application that includes a FastAPI web server and various utilities for data processing and management. It is designed to handle job search functionalities and geographical data processing.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the `backend/python` directory.
3. Create a virtual environment:

   ```bash
python -m venv venv
```

4. Activate the virtual environment:

   - On Windows:

     ```bash
.\venv\Scripts\activate
```

   - On macOS and Linux:

     ```bash
source venv/bin/activate
```

5. Install the required dependencies using pip:

   ```bash
pip install .
```

   This will install all the dependencies specified in the `setup.py` file.

## Usage

- To start the FastAPI application, run:

  ```bash
uvicorn api:app --host 127.0.0.1 --port 10000 --reload
```

- To run the tests, use the following command:

  ```bash
pytest
```

- To run the linter, use the following command:

  ```bash
flake8
```

- To run the formatter, use the following command:

  ```bash
black .
```

- Additional scripts for data extraction and processing can be found in the `geo` and `providers` directories.

## Database Setup

- Import the SQL files located in the `backend` (import.sql) directory into your MySQL database to set up the necessary tables and data.

## Code Examples

- Example of creating a new employer record:

  ```python
from utils.crud import CRUD

crud = CRUD(host='localhost', user='root', password='', database='jobsearch')
crud.create('employers', company_name='Tech Corp', phone_number='1234567890', state='CA', zip_code='90001', email='contact@techcorp.com', password='securepassword', created_at='2023-10-01', updated_at='2023-10-01')
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
