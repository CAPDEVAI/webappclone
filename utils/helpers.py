def get_table_csv_results(pdf_file):
    """Processes a PDF file and extracts table data as CSV."""
    return "column1,column2\nvalue1,value2"
    import boto3
<<<<<<< HEAD
def store_objectIn_s3(bucket_name, object_name, file_path, region_name="us-east-1"):
    """Stores a file in an S3 bucket."""
    s3 = boto3.client("s3", region_name=region_name)
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")
        raise
import boto3
=======
from botocore.exceptions import NoCredentialsError
>>>>>>> 7b7038a (Updated app.py, requirements.txt, and added pdfs directory)

def store_objectIn_s3(file_path, bucket_name, object_key):
    """
    Uploads a file to an AWS S3 bucket.

    Args:
    file_path (str): The path to the file to upload.
    bucket_name (str): The name of the S3 bucket.
    object_key (str): The S3 object key under which to store the file.

    Returns:
    bool: True if file was uploaded successfully, False otherwise.
    """
    s3_client = boto3.client('s3')
    try:
<<<<<<< HEAD
        # Upload the file to S3
=======
>>>>>>> 7b7038a (Updated app.py, requirements.txt, and added pdfs directory)
        with open(file_path, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, object_key)
        print(f"File {file_path} uploaded to {bucket_name} with key {object_key}.")
        return True
<<<<<<< HEAD
    except Exception as e:
        print(f"Failed to upload {file_path} to {bucket_name}: {str(e)}")
        return False
=======
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return False
    except NoCredentialsError:
        print("Error: Credentials not available.")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# Example of another helper function
def get_signed_s3_Object(bucket_name, object_key, expiration=3600):
    """
    Generate a URL to get an object from S3, valid for a specified time.

    Args:
    bucket_name (str): The name of the S3 bucket.
    object_key (str): The S3 object key.
    expiration (int): Time in seconds for the presigned URL to remain valid.

    Returns:
    str: A presigned URL to access the object.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_key},
                                                    ExpiresIn=expiration)
        return response
    except Exception as e:
        print(f"Failed to generate presigned URL: {str(e)}")
        return None
import boto3

def store_objectIn_s3(bucket_name, object_name, file_path, region_name="us-east-1"):
    """Stores a file in an S3 bucket."""
    s3 = boto3.client("s3", region_name=region_name)
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")
        raise
>>>>>>> 7b7038a (Updated app.py, requirements.txt, and added pdfs directory)
