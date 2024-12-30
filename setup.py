import os
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
print(f"ROOT -> {ROOT}")


setup(
    name="AutomotiveVoiceAI",
    version="1.0.0",
    description="Voice AI for automotive industry",
    packages=find_packages(),
    include_package_data=True,
)
