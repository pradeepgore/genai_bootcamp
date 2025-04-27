# filepath: c:\genai_bootcamp\Customer_Support_Agent\setup.py
from setuptools import find_packages, setup

setup(
    name="e-commerce-bot",
    version="0.0.1",
    author="sunny",
    author_email="snshrivas3365@gmail.com",
    packages=find_packages(),
    install_requires=[
        'langchain_astradb',
        'langchain_google_genai',
        'pandas',
        'python-dotenv'
    ]
)