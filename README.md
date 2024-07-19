# Django Excel Upload and Transformation Project

This project is a Django web application that allows users to upload Excel files, transforms the data using a master mapping file, and generates an output file. It also displays a plot of the data.

## Features

- Upload Excel files
- Transform data using a master mapping file
- Generate an output Excel file
- Display a plot of the data

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv myenv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Upload the `input1.xlsx` and `input2.xlsx` files.
- Click the "Generate Output" button to process the files.
- View the generated plot and download the output file.

## Dependencies

- Django
- psycopg2
- pandas
- matplotlib
- plotly
- numpy
- openpyxl
- kaleido

