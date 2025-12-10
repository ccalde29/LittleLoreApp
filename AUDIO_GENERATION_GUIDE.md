# 🎵 Audio Generation System - Complete Setup

## ✅ What's Been Created

### 1. **Story Analysis Script** (`analyze_stories.py`)
- Checks K-5 stories for formatting issues
- Identifies titles in text, URLs, whitespace problems
- Calculates cost estimates for audio generation
- Shows grade and region distribution

### 2. **Story Cleanup Script** (`clean_stories.py`)
- Fixes common text issues automatically
- Removes duplicate paragraphs
- Cleans up whitespace and formatting artifacts
- Validates stories after cleaning
- Safe dry-run mode by default

### 3. **Audio Generation Script** (`generate_audio.py`)
- Uses **Google Cloud Journey voices** (Chirp) - newest, most natural
- Generates MP3 audio files optimized for kids
- Uploads to Supabase storage automatically
- Updates database with audio URLs
- Rate-limited and resumable

### 4. **Database Setup** 
- Created storage bucket for audio files
- Added indexes for faster queries
- Helper functions for batch processing
- Audio statistics tracking

## 🎯 Voice Selection - IMPORTANT!

### ✓ USE THESE (Chirp/Journey):
- **en-US-Journey-F** - Warm, natural female (RECOMMENDED for kids)
- **en-US-Journey-D** - Clear, engaging male
- **en-US-Journey-O** - Expressive female

### ✗ DON'T USE:
- **Neural2 voices** - Older, more robotic
- **Standard voices** - Very basic quality

The Journey voices are Google's newest generation and sound much more natural and expressive - perfect for children's storytelling!

## 💰 Cost Estimates (Your $300 Budget)

Based on typical K-5 story distribution:

| Grade Level | Est. Stories | Avg Length | Total Chars | Est. Cost |
|-------------|--------------|------------|-------------|-----------|
| K-1         | 400-500      | 2,000      | 900K        | $14.40    |
| 2-3         | 500-600      | 4,000      | 2.2M        | $35.20    |
| 4-5         | 300-400      | 7,000      | 2.4M        | $38.40    |
| **TOTAL**   | **1,200-1,500** | -       | **~5.5M**   | **~$88**  |

**You have $300**, so you're well within budget! You could even do multiple voice versions.

## 📋 Step-by-Step Workflow

### Step 1: Initial Setup
```powershell
cd C:\Users\Lizette\OneDrive\Desktop\Projects\LittleLoreApp\scripts
.\setup.ps1
```

This checks:
- ✓ Python installation
- ✓ Required packages
- ✓ Google Cloud credentials
- ✓ Supabase status

### Step 2: Set Up Google Cloud (ONE-TIME)

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**: "LittleLoreApp"
3. **Enable API**:
   - Search: "Cloud Text-to-Speech API"
   - Click "Enable"
4. **Create Service Account**:
   - IAM & Admin > Service Accounts
   - Create "littlelore-tts"
   - Role: "Cloud Text-to-Speech Client"
   - Create JSON key, download it
5. **Set Environment Variable**:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\key.json"
   ```

### Step 3: Analyze Your Stories
```powershell
python analyze_stories.py
```

**Output shows:**
- How many K-5 stories you have
- Stories with formatting issues
- Cost estimates
- Character/word counts

### Step 4: Clean Story Text
```powershell
# Preview changes (safe)
python clean_stories.py

# Apply fixes to database
python clean_stories.py --apply
```

**This fixes:**
- Titles appearing in middle of text
- Excessive whitespace
- URLs and artifacts
- Duplicate paragraphs

### Step 5: Test Audio Generation (SMALL BATCH FIRST!)
```powershell
# Dry run - shows what will happen, no cost
python generate_audio.py --limit 5

# Generate 5 test audio files
python generate_audio.py --limit 5 --apply --voice chirp_female_1
```

**Listen to the test files!** Make sure you like the voice quality before processing everything.

### Step 6: Try Different Voices (Optional)
```powershell
# Try male voice
python generate_audio.py --limit 3 --apply --voice chirp_male_1

# Try alternative female voice
python generate_audio.py --limit 3 --apply --voice chirp_female_2
```

### Step 7: Generate All K-5 Stories
```powershell
# This will process ALL K-5 stories (~$88)
python generate_audio.py --all --apply --voice chirp_female_1
```

**This will take several hours** (rate-limited to 1 story/second for API safety).
You can stop and resume anytime - it only processes stories without audio.

## 📁 File Structure

```
LittleLoreApp/
├── scripts/
│   ├── analyze_stories.py       # Story analysis
│   ├── clean_stories.py         # Story cleanup
│   ├── generate_audio.py        # Audio generation
│   ├── requirements.txt         # Python packages
│   ├── README.md               # Detailed docs
│   ├── setup.ps1               # Quick setup
│   └── project.json            # Config reference
├── audio_files/                 # Local audio (temporary)
├── supabase/
│   └── migrations/
│       ├── 20251210181820_remote_schema.sql    # Base schema
│       └── 20251210_setup_audio_storage.sql    # Audio setup
└── index.html                   # Your app
```

## 🔍 Monitoring Progress

### Check Audio Generation Status
```powershell
# In Supabase Studio (http://127.0.0.1:54323)
# Run this SQL query:

SELECT 
  grade_level,
  COUNT(*) as total,
  COUNT(audio_url) as with_audio,
  COUNT(*) - COUNT(audio_url) as remaining
FROM stories_raw
WHERE grade_level IN ('K-1', '2-3', '4-5')
GROUP BY grade_level;
```

### View Generated Files
- **Local**: `audio_files/` directory
- **Supabase Storage**: http://127.0.0.1:54323 > Storage > audio bucket
- **Database URLs**: Check `stories_raw.audio_url` column

## 🎨 Audio Settings (In generate_audio.py)

Current optimized settings for kids:
```python
speaking_rate=0.95,  # Slightly slower - easier to follow
pitch=0.0,           # Normal pitch
volume_gain_db=0.0,  # Normal volume
effects_profile_id=['headphone-class-device']  # Optimized for headphones
```

To adjust, edit lines 82-86 in `generate_audio.py`.

## 🚨 Important Notes

1. **Start Small**: Always test with 5-10 stories first
2. **Budget Tracking**: Google Cloud Console shows real-time costs
3. **Resume Support**: Script only processes stories without audio
4. **Storage**: Each audio file ~1-2MB, plan storage accordingly
5. **Rate Limits**: 1 story/second keeps you safe from API throttling

## 🆘 Troubleshooting

### "GOOGLE_APPLICATION_CREDENTIALS not set"
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\full\path\to\key.json"
# Restart PowerShell after setting
```

### "Bucket not found"
- Database reset created the bucket automatically
- Check in Supabase Studio: Storage > audio

### "Permission denied"
- Verify service account has "Cloud Text-to-Speech Client" role
- Check JSON key file is readable

### Audio quality issues
- Try different voices (chirp_female_1, chirp_male_1)
- Adjust `speaking_rate` in generate_audio.py
- Make sure you're using Journey voices, not Neural2

## 📊 Success Criteria

After completion, you should have:
- ✓ All K-5 stories with clean text
- ✓ Audio URLs in database
- ✓ MP3 files in Supabase storage
- ✓ Cost under $100 (well within $300 budget)
- ✓ Natural, kid-friendly voice quality

## 🎯 Next Steps

Once audio is generated:
1. Update your HTML app to play audio from database URLs
2. Add playback controls (play/pause, speed)
3. Consider generating multiple voice versions
4. Test with actual kids for feedback
5. Add read-along highlighting feature

---

**Questions?** All scripts have built-in help and dry-run modes. Start with `analyze_stories.py` to see what you're working with!
