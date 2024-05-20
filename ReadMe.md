# Cloudfloat Coding Challenge: Invoice Upload Service

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Setup the Environment**:
    - Ensure Docker and Docker Compose are installed on your machine.
    - Create a `.env` file with the following variables:
      ```plaintext
      DB_NAME=test
      DB_USER=test
      DB_PASSWORD=test
      DB_HOST=db
      DB_PORT=5432
      ```

3. **Build and Run the Docker Containers**:
    ```bash
    docker-compose up --build
    ```

4. **Run Tests**:
    ```bash
    docker-compose run web python manage.py test
    ```

## API Endpoints

- **POST /invoices/upload_invoice**: Uploads an invoice.
- **POST /invoices/monthly_report?month=jan**: Generates a monthly report wherein (month=xxx) 'xxx' is the name of the month

## Assumptions and Improvements

- Assumption: The `timestamp_utc` is provided in ISO 8601 format.
- Improvement: Modified the code to be aligned with PEP8 Standard
- Improvement: Add authentication and authorization for the endpoints.
- Improvement: Added pagination for large datasets in the monthly report.
- Improvement: Added more comprehensive data validation and error handling.
