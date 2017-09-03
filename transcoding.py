"""transcoding example for Google Cloud Storage"""

import os
import shutil
import gzip

from google.cloud import storage
from settings import SERVICE_JSON_FILE, BUCKET_NAME


uncompressed_file = 'test_file.txt'
compressed_file = 'test_file.txt.gz'


def create_text_file():
    """creates file with 1GB size with same text repeating (taken somewhere from internet)"""
    a1 = "abcdefghijklmnopqrstuvwxyz"
    a2 = a1[::-1]
    a = a1 + a2[1:]
    size = 1000000000  # GB
    with open(uncompressed_file, 'w') as f:
        for i in range(1, size, len(a)):
            f.write(a)


def compress():
    with open(uncompressed_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


if __name__ == '__main__':
    if not os.path.exists(uncompressed_file):
        create_text_file()
    if not os.path.exists(compressed_file):
        compress()

    client = storage.Client().from_service_account_json(SERVICE_JSON_FILE)
    bucket = storage.Bucket(client, BUCKET_NAME)

    # create blob object and upload content of compressed file
    blob = bucket.blob(compressed_file, chunk_size=262144 * 10)
    blob.content_encoding = 'gzip'
    blob.upload_from_filename(compressed_file, content_type='text/plain')
    blob.make_public()
    print(blob.public_url)

    # blob_un = bucket.blob(uncompressed_file, chunk_size=262144 * 10)
    # blob_un.upload_from_filename(uncompressed_file, content_type='text/plain')

    # download file
    # s1 = datetime.datetime.now()
    # blob2 = bucket.blob(compressed_file)
    # blob2.make_public()
    # # blob2.download_to_filename('downloaded1.txt')
    # # e1 = datetime.datetime.now()
    # # diff1 = e1-s1
    # # total1 = diff1.total_seconds()
    # #
    # # s2 = datetime.datetime.now()
    # # blob3 = bucket.blob(uncompressed_file)
    # # blob3.download_to_filename('downloaded2.txt')
    # # e2 = datetime.datetime.now()
    # # diff2 = e2 - s2
    # # total2 = diff2.total_seconds()
    # # print("download of compressed file: ", total1)
    # # print("download of uncompressed file: ", total2)
    #
    # s3 = datetime.datetime.now()
    # comp_public_url = blob2.public_url
    # r = requests.get(comp_public_url, stream=True)
    # with open('download3.txt', 'wb') as f:
    #     for chunk in r.iter_content(chunk_size=1024):
    #         if chunk:  # filter out keep-alive new chunks
    #             f.write(chunk)
    #
    # e3 = datetime.datetime.now()
    # diff3 = e3 - s3
    # total2 = diff3.total_seconds()



