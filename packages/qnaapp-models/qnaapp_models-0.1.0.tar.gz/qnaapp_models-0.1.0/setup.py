from setuptools import setup, find_packages

setup(
        name='qnaapp_models',
        version='0.1.0',
        packages=find_packages(),
        setup_requires=['wheel'],
        install_requires=[
            "pydantic",
            "typing",
            "datetime"
],
)