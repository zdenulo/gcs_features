from settings import SERVICE_JSON_FILE, BUCKET_NAME
from google.cloud import storage
from google.auth.transport.requests import AuthorizedSession
from pprint import pprint
from google.oauth2 import service_account

client = storage.Client().from_service_account_json(SERVICE_JSON_FILE)

credentials = service_account.Credentials.from_service_account_file(SERVICE_JSON_FILE)
credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
authed_session = AuthorizedSession(credentials)

bucket = storage.Bucket(client, BUCKET_NAME)

# name of the file which will be created in Cloud Storage
FILENAME = 'test_versioned_file.txt'

# enable versioning for bucket
bucket.enable_logging(BUCKET_NAME)
bucket.versioning_enabled = True
bucket.update()

# upload 3 times different content for the same filename
blob = bucket.blob(FILENAME)
blob.upload_from_string('first version', content_type='text/plain')
blob.upload_from_string('second version', content_type='text/plain')
blob.upload_from_string('third version', content_type='text/plain')

# list all files in the bucket with prefix equals to the filename
blob_versions_url = "https://www.googleapis.com/storage/v1/b/{bucket}/o?versions=true&prefix={filename}".format(bucket=BUCKET_NAME, filename=FILENAME)

# get versions
response = authed_session.get(blob_versions_url)
data = response.json()
versions = data['items']
pprint(versions)
# get first and latest generation
first_generation_url = versions[0]['mediaLink']
last_generation_url = versions[-1]['mediaLink']

resp = authed_session.get(first_generation_url)
pprint(resp.text)

resp = authed_session.get(last_generation_url)
pprint(resp.text)

print("current content ", blob.download_as_string())