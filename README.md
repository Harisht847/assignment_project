# Cloud Storage Application

This Python application helps you organize and upload different types of files to different cloud storage services. It identifies media, image, and document files within a directory and its subdirectories and uploads them to Amazon S3 or Google Cloud Storage based on their type.

## Features

- Identify and categorize media, image, and document files.
- Upload media and image files to Amazon S3.
- (Future feature: Upload document files to Google Cloud Storage.)
- Supports both synchronous and asynchronous file uploads.

## Prerequisites

- Python 3.6+
- `boto3` library (for AWS S3 interaction)
- `google-cloud-storage` library (for Google Cloud Storage interaction)

## Installation

1. Clone the repository:


2. Install the required libraries:


3. Add your AWS S3 credentials and Google Cloud credentials (for future support) to the appropriate environment variables or directly in the code.

## Usage

1. Place your files in the desired directory.
2. Run the application:


3. The application will identify and categorize your files and upload them to the appropriate cloud storage.

## Configuration

- To configure your AWS S3 credentials, modify the `aws_access_key` and `aws_secret_key` in the `app.py` file.
- (Future feature: To configure your Google Cloud credentials, update the `google_credentials_path` and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in the `app.py` file.)
