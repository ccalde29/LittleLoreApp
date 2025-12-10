"""
Story Analysis Script
Analyzes stories in the database for K-5 grade levels
Identifies issues like titles in text, formatting problems, etc.
"""

import os
from supabase import create_client, Client
import re
from collections import defaultdict

# Connect to local Supabase
SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_k5_stories():
    """Fetch K-5 grade stories from database"""
    response = supabase.table('stories_raw').select('*').in_(
        'grade_level', 
        ['K-1', '2-3', '4-5']
    ).execute()
    return response.data

def check_story_issues(story):
    """Check for common issues in story text"""
    issues = []
    text = story.get('text', '')
    title = story.get('title', '')
    
    # Check if title appears in the middle of text
    if title and title in text[len(title)+50:]:  # Skip first occurrence
        issues.append("Title appears in middle of text")
    
    # Check for excessive whitespace
    if '\n\n\n' in text or '   ' in text:
        issues.append("Excessive whitespace")
    
    # Check for URL remnants
    if 'http://' in text or 'https://' in text or 'fairytalez.com' in text:
        issues.append("Contains URLs")
    
    # Check for formatting artifacts
    if '￼' in text or '\x00' in text:
        issues.append("Contains formatting artifacts")
    
    # Check for very short stories (might be incomplete)
    if len(text) < 100:
        issues.append("Story too short (possibly incomplete)")
    
    # Check for very long stories (might have duplicates)
    if len(text) > 50000:
        issues.append("Story very long (possibly duplicated content)")
    
    # Check for repeated paragraphs
    paragraphs = text.split('\n\n')
    if len(paragraphs) != len(set(paragraphs)):
        issues.append("Contains repeated paragraphs")
    
    return issues

def analyze_stories():
    """Main analysis function"""
    print("Fetching K-5 grade stories from local database...")
    stories = get_k5_stories()
    
    print(f"\nFound {len(stories)} stories in K-1, 2-3, and 4-5 grade levels\n")
    
    # Grade level distribution
    grade_dist = defaultdict(int)
    region_dist = defaultdict(int)
    stories_with_issues = []
    
    for story in stories:
        grade = story.get('grade_level', 'Unknown')
        region = story.get('region', 'Unknown')
        grade_dist[grade] += 1
        region_dist[region] += 1
        
        issues = check_story_issues(story)
        if issues:
            stories_with_issues.append({
                'story_id': story.get('story_id'),
                'title': story.get('title'),
                'grade': grade,
                'issues': issues
            })
    
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
    
    print("\n" + "=" * 70)
    print(f"STORIES WITH ISSUES: {len(stories_with_issues)}")
    print("=" * 70)
    
    if stories_with_issues:
        print(f"\nShowing first 20 stories with issues:\n")
        for i, story_info in enumerate(stories_with_issues[:20], 1):
            print(f"{i}. [{story_info['grade']}] {story_info['title'][:50]}")
            for issue in story_info['issues']:
                print(f"   - {issue}")
            print()
    
    # Calculate text-to-speech estimates
    total_chars = sum(len(story.get('text', '')) for story in stories)
    total_words = sum(len(story.get('text', '').split()) for story in stories)
    
    print("=" * 70)
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
    print(f"  ~{int((75000000 / total_chars) * len(stories))} stories at current average length")
    
    return stories, stories_with_issues

if __name__ == "__main__":
    try:
        stories, issues = analyze_stories()
        
        # Save results to file
        with open('story_analysis_results.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total K-5 Stories: {len(stories)}\n")
            f.write(f"Stories with issues: {len(issues)}\n\n")
            for story_info in issues:
                f.write(f"\nStory ID: {story_info['story_id']}\n")
                f.write(f"Title: {story_info['title']}\n")
                f.write(f"Grade: {story_info['grade']}\n")
                f.write(f"Issues: {', '.join(story_info['issues'])}\n")
        
        print("\n✓ Analysis saved to story_analysis_results.txt")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Supabase is running (supabase status)")
        print("  2. Python packages are installed (pip install supabase)")
