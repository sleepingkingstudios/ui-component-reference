# Hydra

A [Flask](https://flask.palletsprojects.com/en/3.0.x/) tool for evaluating and comparing design systems.

## Local Development

1.  Activate the `venv` Virtual Environment:

    ```bash
    . .venv/bin/activate
    ```

2.  Install the application:

    ```bash
    pip install -e .
    ```

3.  Run the application:

    ```bash
    flask --app hydra run --port=3000 --debug
    ```

    > @note: The default port 5000 is not recommended on macOS devices due to a
    >   conflict with Airdrop services.

4.  Run the unit tests:

    ```bash
    pytest
    ```

5.  Run the code linter:

    ```bash
    flake8 hydra
    ```
