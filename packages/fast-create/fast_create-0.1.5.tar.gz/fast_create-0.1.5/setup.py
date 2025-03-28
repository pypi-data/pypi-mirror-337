from setuptools import setup, find_packages
from version import version

setup(
    name="fast-create",
    version=version,
    packages=find_packages(),
    include_package_data=True,  
    package_data={"fast_create": ["temp/**/*"]}, 
    py_modules=["fast_create"],
    install_requires=[
    'fastapi[all]', 'uvicorn', 'python-dotenv', 'psycopg2-binary', 
    'sqlmodel', 'fastapi_mail', 'pydantic', 'python-jose[cryptography]', 
    'oauth2', 'passlib', 'sqlalchemy'
    ],
    entry_points={
        "console_scripts": [
            "fast-create=fast_create:main",
        ],
    },
)
