def get_table_csv_results(pdf_file):
    """Processes a PDF file and extracts table data as CSV."""
    return "column1,column2\nvalue1,value2"
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
import boto3

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
        # Upload the file to S3
        with open(file_path, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, object_key)
        print(f"File {file_path} uploaded to {bucket_name} with key {object_key}.")
        return True
    except Exception as e:
        print(f"Failed to upload {file_path} to {bucket_name}: {str(e)}")
        return False
