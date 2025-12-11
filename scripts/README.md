# Audio Generation Setup for Little Lores App

This guide will help you set up Google Cloud Text-to-Speech to generate audio files for your K-5 grade stories.

## 🎯 Overview

We're using **Google Cloud Journey voices** (also called "Chirp" voices) - the newest and most natural-sounding voices from Google. These are specifically great for children's content.

## 📋 Prerequisites

1. **Google Cloud Account** with $300 free credits
2. **Python 3.8+** installed
3. **Supabase** running locally

## 🚀 Setup Steps

### 1. Install Python Dependencies

```powershell
cd C:\Users\Lizette\OneDrive\Desktop\Projects\LittleLoreApp\scripts
pip install -r requirements.txt
```

### 2. Set Up Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Cloud Text-to-Speech API**:
   - Search for "Text-to-Speech API"
   - Click "Enable"
4. Create service account credentials:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Name it "littlelore-tts"
   - Grant role: "Cloud Text-to-Speech Client"
   - Click "Create Key" > JSON
   - Save the JSON file securely

### 3. Set Environment Variable

```powershell
# Set for current session
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"

# Or set permanently
[System.Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'C:\path\to\your\key.json', 'User')
```

### 4. Verify Google Cloud Storage Bucket

The scripts use your existing GCS bucket `little-lore-audio`:

1. Verify bucket exists in [Google Cloud Console](https://console.cloud.google.com/storage)
2. Make sure your service account has permissions:
   - Storage Object Admin (to upload files)
   - Storage Object Viewer (to read files)
3. Bucket should be publicly accessible for audio playback
4. Location: Choose closest to your users (e.g., us-central1)

## 📊 Step-by-Step Workflow

### Step 1: Analyze Stories

This checks your K-5 stories for issues:

```powershell
python analyze_stories.py
```

**Output:**
- Grade level distribution
- Stories with formatting issues
- Cost estimates for audio generation

### Step 2: Clean Stories

This fixes common issues (titles in text, extra whitespace, URLs, etc.):

```powershell
# Dry run (preview changes)
python clean_stories.py

# Apply changes to database
python clean_stories.py --apply
```

### Step 3: Generate Audio (Test First!)

Start with a small batch to test:

```powershell
# Test with 5 stories (dry run to see cost)
python generate_audio.py --limit 5

# Generate audio for 5 stories
python generate_audio.py --limit 5 --apply

# Try different voices
python generate_audio.py --limit 5 --apply --voice chirp_female_1
python generate_audio.py --limit 5 --apply --voice chirp_male_1
```

### Step 4: Generate All K-5 Stories

Once you're happy with the test results:

```powershell
# Generate all K-5 stories
python generate_audio.py --all --apply --voice chirp_female_1
```

## 🎙️ Available Voices

The scripts use **Journey voices** (Chirp) - the newest Google Cloud TTS voices:

| Voice Key | Voice Name | Description |
|-----------|------------|-------------|
| `chirp_female_1` | en-US-Journey-F | Warm, natural female - RECOMMENDED |
| `chirp_male_1` | en-US-Journey-D | Clear, engaging male |
| `chirp_female_2` | en-US-Journey-O | Expressive female |
| `studio_female` | en-US-Studio-O | Studio quality female (fallback) |
| `studio_male` | en-US-Studio-M | Studio quality male (fallback) |

**Note:** Journey/Chirp voices are much more natural than Neural2 voices. Neural2 is older and more robotic.

## 💰 Cost Estimates (K-5 Stories Only)

Based on your database:
- **Chirp/Journey voices**: $16 per 1M characters
- **Your $300 credits**: ~18.75M characters
- **Average story**: ~5,000 characters

**Estimated costs for K-5 grades:**
- You likely have ~1,000-1,500 K-5 stories
- Total characters: ~5-7M characters
- **Total cost: ~$80-$112** (well within your $300 budget!)

## 🔧 Troubleshooting

### "GOOGLE_APPLICATION_CREDENTIALS not set"
- Make sure you've set the environment variable
- Restart PowerShell after setting it

### "Permission denied" errors
- Check your service account has "Cloud Text-to-Speech Client" role
- Verify the JSON key file is readable

### "Bucket not found" errors
- Verify `little-lore-audio` bucket exists in Google Cloud Storage
- Check service account has Storage Object Admin permissions
- Make sure bucket is publicly accessible

### Audio quality issues
- Try different voices (chirp_female_1, chirp_male_1)
- Adjust `speaking_rate` in generate_audio.py (default: 0.95)
- Adjust `pitch` for different tones

## 📁 Generated Files

- `audio_files/` - Local MP3 files (before upload)
- `story_analysis_results.txt` - Story analysis report
- Audio files uploaded to: `gs://little-lore-audio/story-audio/{story_id}.mp3`
- Public URLs stored in database: `stories_raw.audio_url`

## 🎯 Next Steps

After generating audio:
1. Update your HTML app to use the audio URLs from database
2. Test playback in browser
3. Consider adding:
   - Play/pause controls
   - Speed controls
   - Multiple voice options per story
   - Read-along highlighting

## 📝 Notes

- Audio generation is rate-limited to 1 story per second (be nice to API)
- Files are ~1-2MB per story (plan storage accordingly)
- Stories are processed in batches (can resume if interrupted)
- Audio URLs are automatically saved to `stories_raw.audio_url`

## 🆘 Support

If you encounter issues:
1. Check Supabase is running: `supabase status`
2. Verify Google Cloud credentials are valid
3. Check API quotas in Google Cloud Console
4. Review error messages in console output
