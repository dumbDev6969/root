# Contributing to the JobSearch API

Thank you for your interest in contributing to the JobSearch API project. This document outlines the improvements we've made and provides guidelines for contributors to ensure consistent and high-quality code.

## Recent Improvements

1. **Code Organization**: CRUD operations have been separated into individual files (`create.py`, `read.py`, `update.py`, `delete.py`) with a centralized `database.py` file for database connections.

2. **Password Management**: We now use the Argon2 algorithm for secure password hashing and verification (`password_manager.py`).

3. **Encryption**: The encryption mechanism has been improved with persistent keys and enhanced error handling (`encryption.py`).

4. **Error Handling**: A centralized error handling system has been implemented (`error_handler.py`) and integrated into the main `api.py` file.

5. **Logging**: We use a consistent logging approach throughout the application.

6. **API Documentation**: Detailed docstrings have been added to routes in `api.py` for better API documentation.

7. **Testing**: A `tests` directory has been added with basic unit and integration tests.

8. **Code Formatting**: Black has been set up for consistent code formatting.

## Development Guidelines

### Setting Up the Development Environment

1. Clone the repository and navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

### Running Tests

To run the tests, use the following command in the `backend` directory:

```
pytest
```

### Code Formatting

We use Black for code formatting. To format your code, run:

```
black .
```

in the `backend` directory.

### Adding New Features or Fixing Bugs

1. Create a new branch for your feature or bug fix.
2. Write tests for your changes in the `tests` directory.
3. Implement your changes, ensuring they pass all tests.
4. Format your code using Black.
5. Update the API documentation if you've modified or added endpoints.
6. Submit a pull request with a clear description of your changes.

### Best Practices

- Follow PEP 8 style guide for Python code.
- Write clear, concise commit messages.
- Keep functions and methods small and focused on a single task.
- Use type hints to improve code readability and catch potential type-related errors.
- Document your code using docstrings and inline comments where necessary.
- Handle exceptions appropriately and use the centralized error handling system.
- Use environment variables for sensitive information (e.g., database credentials, API keys).

By following these guidelines, we can maintain a high-quality, consistent codebase that is easy to understand and contribute to. Thank you for your contributions!
