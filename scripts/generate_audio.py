"""
Google Cloud Text-to-Speech Script
Generates audio files for K-5 grade stories using Chirp voices
Uploads to Supabase storage
"""

import os
from google.cloud import texttospeech
from supabase import create_client, Client
import time
from pathlib import Path

# Supabase connection
SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Google Cloud TTS Chirp Voices (newest generation)
# These are the best voices for children's content - natural, expressive, and clear
AVAILABLE_VOICES = {
    'chirp_female_1': {
        'name': 'en-US-Journey-F',  # Chirp female voice
        'gender': texttospeech.SsmlVoiceGender.FEMALE,
        'description': 'Natural, warm female voice - great for storytelling'
    },
    'chirp_male_1': {
        'name': 'en-US-Journey-D',  # Chirp male voice
        'gender': texttospeech.SsmlVoiceGender.MALE,
        'description': 'Clear, engaging male voice - excellent for narration'
    },
    'chirp_female_2': {
        'name': 'en-US-Journey-O',  # Another Chirp female
        'gender': texttospeech.SsmlVoiceGender.FEMALE,
        'description': 'Expressive female voice - perfect for character stories'
    },
    # Fallback to Studio voices if Chirp not available
    'studio_female': {
        'name': 'en-US-Studio-O',
        'gender': texttospeech.SsmlVoiceGender.FEMALE,
        'description': 'Studio quality female voice'
    },
    'studio_male': {
        'name': 'en-US-Studio-M',
        'gender': texttospeech.SsmlVoiceGender.MALE,
        'description': 'Studio quality male voice'
    }
}

def setup_google_credentials():
    """Check for Google Cloud credentials"""
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("⚠ GOOGLE_APPLICATION_CREDENTIALS not set!")
        print("\nTo set up Google Cloud TTS:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Cloud Text-to-Speech API")
        print("4. Create a service account and download JSON key")
        print("5. Set environment variable:")
        print('   $env:GOOGLE_APPLICATION_CREDENTIALS="path\\to\\your\\key.json"')
        return False
    
    if not os.path.exists(creds_path):
        print(f"⚠ Credentials file not found: {creds_path}")
        return False
    
    print(f"✓ Google Cloud credentials found: {creds_path}")
    return True

def list_available_voices():
    """List all available voices from Google Cloud TTS"""
    try:
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices()
        
        print("\n" + "=" * 70)
        print("AVAILABLE GOOGLE CLOUD TTS VOICES")
        print("=" * 70)
        
        # Filter for English voices
        en_voices = [v for v in voices.voices if 'en-US' in v.language_codes]
        
        # Group by voice type
        chirp_voices = [v for v in en_voices if 'Journey' in v.name]
        studio_voices = [v for v in en_voices if 'Studio' in v.name]
        neural2_voices = [v for v in en_voices if 'Neural2' in v.name]
        
        print(f"\n🎯 CHIRP VOICES (Journey - RECOMMENDED):")
        for v in chirp_voices[:10]:
            print(f"  {v.name:30} - {v.ssml_gender.name}")
        
        print(f"\n🎙️  STUDIO VOICES (High Quality):")
        for v in studio_voices[:5]:
            print(f"  {v.name:30} - {v.ssml_gender.name}")
        
        print(f"\n🤖 NEURAL2 VOICES (Older - NOT RECOMMENDED):")
        for v in neural2_voices[:3]:
            print(f"  {v.name:30} - {v.ssml_gender.name}")
        
        return True
    except Exception as e:
        print(f"✗ Error listing voices: {e}")
        return False

def generate_audio(text, story_id, voice_config, output_dir='audio_files'):
    """Generate audio file using Google Cloud TTS"""
    try:
        client = texttospeech.TextToSpeechClient()
        
        # Set up the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Configure voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_config['name']
        )
        
        # Configure audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.95,  # Slightly slower for kids
            pitch=0.0,
            volume_gain_db=0.0,
            effects_profile_id=['headphone-class-device']  # Optimized for headphones
        )
        
        # Generate audio
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Save to file
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filename = f"{story_id}.mp3"
        filepath = output_path / filename
        
        with open(filepath, 'wb') as out:
            out.write(response.audio_content)
        
        return str(filepath)
    
    except Exception as e:
        print(f"✗ Error generating audio: {e}")
        return None

def upload_to_supabase_storage(filepath, story_id):
    """Upload audio file to Supabase storage"""
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # Upload to storage bucket
        storage_path = f"story-audio/{story_id}.mp3"
        
        supabase.storage.from_('audio').upload(
            storage_path,
            file_data,
            file_options={"content-type": "audio/mpeg"}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('audio').get_public_url(storage_path)
        
        # Update story record with audio URL
        supabase.table('stories_raw').update({
            'audio_url': public_url
        }).eq('story_id', story_id).execute()
        
        return public_url
    
    except Exception as e:
        print(f"✗ Error uploading to Supabase: {e}")
        return None

def process_k5_stories(voice_key='chirp_female_1', limit=None, dry_run=True):
    """Process K-5 stories and generate audio"""
    
    if not setup_google_credentials():
        return
    
    # List available voices
    list_available_voices()
    
    print("\n" + "=" * 70)
    print("PROCESSING K-5 STORIES")
    print("=" * 70)
    
    voice_config = AVAILABLE_VOICES.get(voice_key)
    if not voice_config:
        print(f"✗ Invalid voice key: {voice_key}")
        print(f"Available: {', '.join(AVAILABLE_VOICES.keys())}")
        return
    
    print(f"\nUsing voice: {voice_config['name']}")
    print(f"Description: {voice_config['description']}")
    
    # Fetch K-5 stories without audio
    query = supabase.table('stories_raw').select('*').in_(
        'grade_level', 
        ['K-1', '2-3', '4-5']
    ).is_('audio_url', 'null')
    
    if limit:
        query = query.limit(limit)
    
    response = query.execute()
    stories = response.data
    
    print(f"\nFound {len(stories)} stories without audio")
    
    if dry_run:
        print("\n⚠ DRY RUN - No audio will be generated")
        print("Run with dry_run=False to generate audio\n")
        
        # Show cost estimate
        total_chars = sum(len(s.get('text', '')) for s in stories)
        print(f"Total characters: {total_chars:,}")
        print(f"Estimated cost: ${(total_chars / 1000000) * 16:.2f}")
        return
    
    # Process each story
    for i, story in enumerate(stories, 1):
        story_id = story.get('story_id')
        title = story.get('title', '')
        text = story.get('text', '')
        
        print(f"\n[{i}/{len(stories)}] Processing: {title[:50]}")
        print(f"  Characters: {len(text):,}")
        
        # Generate audio
        print(f"  Generating audio with {voice_config['name']}...")
        filepath = generate_audio(text, story_id, voice_config)
        
        if filepath:
            file_size = os.path.getsize(filepath) / 1024 / 1024  # MB
            print(f"  ✓ Audio generated: {file_size:.2f} MB")
            
            # Upload to Supabase
            print(f"  Uploading to Supabase storage...")
            url = upload_to_supabase_storage(filepath, story_id)
            
            if url:
                print(f"  ✓ Uploaded successfully")
            else:
                print(f"  ✗ Upload failed")
        else:
            print(f"  ✗ Audio generation failed")
        
        # Rate limiting (be nice to API)
        if i < len(stories):
            time.sleep(1)
    
    print("\n✓ Processing complete!")

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    dry_run = True
    voice = 'chirp_female_1'
    limit = 5  # Default to 5 stories for testing
    
    if '--apply' in sys.argv:
        dry_run = False
    
    if '--voice' in sys.argv:
        idx = sys.argv.index('--voice')
        if idx + 1 < len(sys.argv):
            voice = sys.argv[idx + 1]
    
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    
    if '--all' in sys.argv:
        limit = None
    
    print("Google Cloud Text-to-Speech - Story Audio Generator")
    print("=" * 70)
    
    if dry_run:
        print("Mode: DRY RUN (use --apply to generate audio)")
    else:
        print("Mode: LIVE (will generate audio and upload)")
    
    print(f"Voice: {voice}")
    print(f"Limit: {limit if limit else 'All stories'}")
    print()
    
    process_k5_stories(voice_key=voice, limit=limit, dry_run=dry_run)
