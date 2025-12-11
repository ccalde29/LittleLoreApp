"""
Google Cloud Storage Setup Verification
Checks that your GCS bucket and permissions are configured correctly
"""

import os
from google.cloud import storage

GCS_BUCKET_NAME = "little-lores-audio"

def check_gcs_setup():
    """Verify Google Cloud Storage configuration"""
    
    print("=" * 70)
    print("Google Cloud Storage Setup Verification")
    print("=" * 70)
    print()
    
    # Check credentials
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("✗ GOOGLE_APPLICATION_CREDENTIALS not set!")
        print("  Set with: $env:GOOGLE_APPLICATION_CREDENTIALS='path\\to\\key.json'")
        return False
    
    if not os.path.exists(creds_path):
        print(f"✗ Credentials file not found: {creds_path}")
        return False
    
    print(f"✓ Credentials found: {creds_path}")
    print()
    
    try:
        # Initialize storage client
        storage_client = storage.Client()
        print(f"✓ Successfully authenticated with Google Cloud")
        print(f"  Project: {storage_client.project}")
        print()
        
        # Check bucket exists
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        if bucket.exists():
            print(f"✓ Bucket '{GCS_BUCKET_NAME}' exists")
        else:
            print(f"✗ Bucket '{GCS_BUCKET_NAME}' not found!")
            print("  Create it at: https://console.cloud.google.com/storage")
            return False
        
        # Get bucket details
        bucket.reload()
        print(f"  Location: {bucket.location}")
        print(f"  Storage class: {bucket.storage_class}")
        print()
        
        # Test write permission
        print("Testing write permissions...")
        test_blob = bucket.blob("test-permission.txt")
        test_blob.upload_from_string("test", content_type="text/plain")
        print("✓ Write permission verified")
        
        # Test public access
        test_blob.make_public()
        public_url = test_blob.public_url
        print(f"✓ Public access enabled")
        print(f"  Test URL: {public_url}")
        
        # Clean up test file
        test_blob.delete()
        print("✓ Cleanup successful")
        print()
        
        # Check if story-audio folder exists
        blobs = list(bucket.list_blobs(prefix="story-audio/", max_results=5))
        if blobs:
            print(f"✓ Found {len(blobs)} existing audio files in story-audio/")
            for blob in blobs[:3]:
                print(f"  - {blob.name}")
        else:
            print("ℹ No existing audio files found (this is normal for fresh setup)")
        print()
        
        print("=" * 70)
        print("✓ Google Cloud Storage is configured correctly!")
        print("=" * 70)
        print()
        print("You're ready to generate audio files!")
        print("Run: python generate_audio.py --limit 5 --apply")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPossible issues:")
        print("  - Service account doesn't have 'Storage Object Admin' role")
        print("  - Bucket doesn't exist or is in a different project")
        print("  - Network/firewall issues")
        return False

if __name__ == "__main__":
    try:
        check_gcs_setup()
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install google-cloud-storage")
