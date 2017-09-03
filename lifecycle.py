
"""setting lifecycle for bucket"""

from google.cloud import storage

from settings import SERVICE_JSON_FILE, BUCKET_NAME

client = storage.Client().from_service_account_json(SERVICE_JSON_FILE)
bucket = storage.Bucket(client, BUCKET_NAME)

rules = [
    {
        'action': {
            'type': 'SetStorageClass',
            'storageClass': 'COLDLINE'
        },
        'condition': {
            'age': 365
        }
    },

    {
        'action': {
            'type': 'Delete'
        },
        'condition': {
            'age': 365*10,
            'matchesStorageClass': ['COLDLINE']
        }
    }
]

bucket.lifecycle_rules = rules
bucket.update()