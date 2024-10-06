# qa-activity08
Repo for Quality Assurance course of Activity 08

# Test Login

The project used to test the login functionality was a project done for a University course, check it in this [repo](https://github.com/ERodbot/LabFlow).

# Test shopping

The project used to test the shopping functionality was an ecommerce project found online, you can check it out [here](https://github.com/evershopcommerce/evershop).

# Running the project

Python version: `3.12.2`

It is best practice to setup a virtual environment to work with Python projects, for more information on how to [make a virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

## Virtual Environment quick guide

1. `python -m venv venv`
For Windows:
2. `venv\Scripts\activate`
For MacOS/Linux
2. `soruce venv/bin.activate`
3. `pip install -r requirements.txt`

To deactivate the virtual environment:
4. `deactivate`

Run the following command to install the needed dependencies:
```bash
pip install -r requirements.txt
```

After installing the dependencies, run the following command to test:

```bash
# Test login (need to deploy the LabFlow project locally)
python test-login.py
# Test shopping
python test-shopping.py
```