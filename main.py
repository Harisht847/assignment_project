

import os
import boto3
from google.cloud import storage
import concurrent.futures
import asyncio
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)






aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


# Google Cloud Storage

google_credentials_path = 'path/to/your/google/credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials_path
gcs_client = storage.Client()



def upload_to_s3(file_path, bucket_name="cloudstorageappfiles"):
    """
    Uploads a file to AWS S3 bucket.

    Args:
        file_path (str): Path to the file to be uploaded.
        bucket_name (str, optional): Name of the S3 bucket. Defaults to "cloudstorageappfiles".
    """

    s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
    logger.info(f'File --> {file_path} has been uploaded successfully....')

def upload_to_gcs(file_path, bucket_name):
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)



class DirectoryReader:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def _get_files_recursive(self):
        all_files = []
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files

    def get_all_files(self):
        return self._get_files_recursive()

    def get_files_by_extension(self, extension):
        extension = extension.lower()
        all_files = self._get_files_recursive()
        matching_files = [file for file in all_files if file.lower().endswith(extension)]
        return matching_files

    def get_files_by_type(self, file_type):
        file_type = file_type.lower()
        all_files = self._get_files_recursive()

        if file_type == 'media':
            media_extensions = ['.mp3', '.mp4', '.avi', '.mov', '.wav']
            matching_files = [file for file in all_files if any(file.lower().endswith(ext) for ext in media_extensions)]
        elif file_type == 'document':
            document_extensions = ['.txt', '.doc', '.pdf', '.xlsx', '.pptx']
            matching_files = [file for file in all_files if any(file.lower().endswith(ext) for ext in document_extensions)]
        elif file_type == 'image':
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            matching_files = [file for file in all_files if any(file.lower().endswith(ext) for ext in image_extensions)]
        else:
            matching_files = []

        return matching_files

class FileTypeIdentifier:
    MEDIA_EXTENSIONS = ['.mp3', '.mp4', '.avi', '.mov', '.wav']
    DOCUMENT_EXTENSIONS = ['.txt', '.doc', '.pdf', '.xlsx', '.pptx']
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    def get_file_type(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension in FileTypeIdentifier.MEDIA_EXTENSIONS:
            return 'Media'
        elif extension in FileTypeIdentifier.DOCUMENT_EXTENSIONS:
            return 'Document'
        elif extension in FileTypeIdentifier.IMAGE_EXTENSIONS:
            return 'Image'
        else:
            return 'Unknown'

def upload_files_parallel(files, file_type):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for file in files:
            ftype = file_type.get_file_type(file)
            if ftype == 'Media' or ftype == 'Image':
                executor.submit(upload_to_s3, file)
            elif ftype == "Document":
                executor.submit(upload_to_s3, file)
            
    

def run_parallel(directory_path):
    reader = DirectoryReader(directory_path)
    files = reader.get_all_files()
    fype_identifier = FileTypeIdentifier()
    upload_files_parallel(files,fype_identifier)


def run():
    reader = DirectoryReader(r'C:\Users\DELL\Desktop\app')
    files = reader.get_all_files()
    file_type = FileTypeIdentifier()
    print(files)

    for file in files:
        ftype = file_type.get_file_type(file)
        if ftype == 'Media' or ftype == 'Image':
            upload_to_s3(file)
        elif ftype == "Document":
            pass


async def upload_file_async(file, file_type):
    """
    Uploads a file asynchronously to AWS S3 based on its type.

    Args:
        file (str): Path to the file to be uploaded.
        file_type (FileTypeIdentifier): Instance of FileTypeIdentifier for identifying file type.
    """
    ftype = file_type.get_file_type(file)
    if ftype == 'Media' or ftype == 'Image':
        await loop.run_in_executor(None, upload_to_s3, file)
        logger.info(f'File "{file}" has been uploaded asynchronously to S3.')
        



async def main():
    """
    Main coroutine for asynchronous file uploads.
    """
    reader = DirectoryReader(r'C:\Users\DELL\Desktop\app')
    files = reader.get_all_files()
    ftype = FileTypeIdentifier()
    tasks = [upload_file_async(file,ftype) for file in files]

    # Limit the number of concurrent tasks to prevent overload
    concurrency_limit = 5
    async with asyncio.Semaphore(concurrency_limit):
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    import time
    loop = asyncio.get_event_loop()
    t1 = time.time()
    loop.run_until_complete(main())
    t2 = time.time()
    logger.info(f'Asyncio approach completed in {t2 - t1:.2f} seconds.')

    t1 = time.time()
    run()
    t2 = time.time()
    logger.info(f'Regular approach completed in {t2 - t1:.2f} seconds.')

    t1 = time.time()
    run_parallel(r'C:\Users\DELL\Desktop\app')
    t2 = time.time()
    logger.info(f'Cuncurrent approach completed in {t2 - t1:.2f} seconds.')

