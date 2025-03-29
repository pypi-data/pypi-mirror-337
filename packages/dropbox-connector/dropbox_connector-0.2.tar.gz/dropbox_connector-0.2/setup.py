from setuptools import setup, find_packages

setup(
    name='dropbox_connector',
    version='0.2',
    packages=find_packages(include=["cloud.storage.dropbox_connector", "file.util.pdfparser.pdfreader", "file.util.docxparser.docxreader"]),
    install_requires=[
        "dropbox",
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "PyYAML"
    ],
    author="Sai Kiran Kyama",
    author_email="saikiran41101@gmail.com",
    description="A Python package for Dropbox integration",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)