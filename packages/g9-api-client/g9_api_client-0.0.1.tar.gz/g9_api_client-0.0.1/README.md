# G9 API Client

G9 API Client is a Python library for interacting with the G9 API. It allows you to log in, retrieve contracts, and get the latest invoices and consumption data for electricity and gas.

## Installation

You can install the G9 API Client using pip:

```sh
pip install g9_api_client
```

## Usage

Here is an example of how to use the G9 API Client:

```python
from g9_api_client import G9

def main():
    acc = G9("your_username", "your_password")

    if acc.login():
        print("Login successful")
        contracts = acc.get_contracts()
        if contracts:
            contract_id = contracts[0].get('id')
            print("Contracts:", contracts)
            print("Last Invoice:", acc.get_last_invoice(contract_id))
            print("Last Electricity Consumption:", acc.get_last_electricity_consumption(contract_id))
            print("Last Gas Consumption:", acc.get_last_gas_consumption(contract_id))
        else:
            print("No contracts found")
    else:
        print("Login failed")

if __name__ == "__main__":
    main()
```

## Methods

### `login()`
Logs in to the G9 API using the provided username and password.

### `get_contracts()`
Retrieves the list of contracts associated with the logged-in user.

### `get_last_invoice(contract_id)`
Retrieves the last invoice for the specified contract.

### `get_last_electricity_consumption(contract_id)`
Retrieves the last electricity consumption data for the specified contract.

### `get_last_gas_consumption(contract_id)`
Retrieves the last gas consumption data for the specified contract.

## License

This project is licensed under the Apache 2 License.
