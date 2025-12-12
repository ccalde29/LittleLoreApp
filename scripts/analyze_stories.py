"""
Story Analysis Script
Analyzes stories in the database for K-5 grade levels
Shows distribution and cost estimates for audio generation
"""

import os
from supabase import create_client, Client
from collections import defaultdict

# Connect to remote Supabase
SUPABASE_URL = "https://mxjhvjwjgqmavmasfypa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14amh2andqZ3FtYXZtYXNmeXBhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3Njk5NjEsImV4cCI6MjA2MDM0NTk2MX0.LLk01H7ueKFPMFpZfNOv3zx8VsICu6Gh6msuSjBW2x0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_k5_stories():
    """Fetch K-5 grade stories from database"""
    response = supabase.table('stories_raw').select('*').in_(
        'grade_level', 
        ['K-1', '2-3', '4-5']
    ).execute()
    return response.data

def analyze_stories():
    """Main analysis function"""
    print("Fetching K-5 grade stories from remote database...")
    stories = get_k5_stories()
    
    print(f"\nFound {len(stories)} stories in K-1, 2-3, and 4-5 grade levels\n")
    
    # Grade level distribution
    grade_dist = defaultdict(int)
    region_dist = defaultdict(int)
    
    for story in stories:
        grade = story.get('grade_level', 'Unknown')
        region = story.get('region', 'Unknown')
        grade_dist[grade] += 1
        region_dist[region] += 1
    
    # Print statistics
    print("=" * 70)
    print("GRADE LEVEL DISTRIBUTION")
    print("=" * 70)
    for grade, count in sorted(grade_dist.items()):
        print(f"{grade:10} : {count:4} stories")
    
    print(f"\n{'Total K-5':10} : {len(stories):4} stories")
    
    print("\n" + "=" * 70)
    print("REGION DISTRIBUTION (K-5 only)")
    print("=" * 70)
    for region, count in sorted(region_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"{region:20} : {count:4} stories")
    
    # Calculate text-to-speech estimates
    total_chars = sum(len(story.get('text', '')) for story in stories)
    total_words = sum(len(story.get('text', '').split()) for story in stories)
    
    print("\n" + "=" * 70)
    print("TEXT-TO-SPEECH ESTIMATES")
    print("=" * 70)
    print(f"Total characters: {total_chars:,}")
    print(f"Total words:      {total_words:,}")
    print(f"\nGoogle Cloud TTS Pricing (as of 2024):")
    print(f"  Standard voices:  $4 per 1M characters")
    print(f"  Neural2 voices:   $16 per 1M characters")
    print(f"  Studio voices:    $16 per 1M characters")
    print(f"  Chirp voices:     $16 per 1M characters")
    print(f"\nEstimated cost for K-5 stories:")
    print(f"  Standard:  ${(total_chars / 1000000) * 4:.2f}")
    print(f"  Neural2:   ${(total_chars / 1000000) * 16:.2f}")
    print(f"  Chirp:     ${(total_chars / 1000000) * 16:.2f}")
    print(f"\nWith $300 credits, you can process:")
    print(f"  ~75M characters with Neural2/Chirp voices")
    if total_chars > 0:
        print(f"  ~{int((75000000 / total_chars) * len(stories))} stories at current average length")
    else:
        print(f"  (Add stories to calculate capacity)")
    
    return stories

if __name__ == "__main__":
    try:
        stories = analyze_stories()
        
        # Save results to file
        with open('story_analysis_results.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total K-5 Stories: {len(stories)}\n")
            f.write(f"Total characters: {sum(len(s.get('text', '')) for s in stories):,}\n")
            f.write(f"Total words: {sum(len(s.get('text', '').split()) for s in stories):,}\n")
        
        if len(stories) > 0:
            print("\n✓ Analysis saved to story_analysis_results.txt")
        else:
            print("\nℹ️  No K-5 stories found in database. Make sure:")
            print("  1. Database connection is working")
            print("  2. Stories are loaded in the stories_raw table")
            print("  3. Stories have grade_level set to 'K-1', '2-3', or '4-5'")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Database connection is working")
        print("  2. Python packages are installed (pip3 install -r requirements.txt)")
