"""
Story Cleanup Script
Cleans and validates K-5 grade stories
Removes formatting issues, duplicate content, and other problems
"""

import os
from supabase import create_client, Client
import re

# Connect to local Supabase
SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_text(text, title):
    """Clean story text"""
    if not text:
        return text
    
    # Remove URLs
    text = re.sub(r'https?://[^\s]+', '', text)
    
    # Remove formatting artifacts
    text = text.replace('￼', '')
    text = text.replace('\x00', '')
    
    # Fix excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
    text = re.sub(r' {3,}', ' ', text)  # Max 2 spaces
    
    # Remove title from middle of text (keep only first occurrence if at start)
    if title and title in text:
        # If title is at the very beginning, that's fine
        if text.startswith(title):
            # Remove subsequent occurrences
            first_occurrence = text.find(title)
            rest_of_text = text[first_occurrence + len(title):]
            text = title + rest_of_text.replace(title, '')
        else:
            # Remove all occurrences if not at start
            text = text.replace(title, '')
    
    # Remove duplicate paragraphs
    paragraphs = text.split('\n\n')
    seen = set()
    unique_paragraphs = []
    for para in paragraphs:
        para_clean = para.strip()
        if para_clean and para_clean not in seen:
            seen.add(para_clean)
            unique_paragraphs.append(para)
    text = '\n\n'.join(unique_paragraphs)
    
    # Clean up spacing
    text = text.strip()
    
    return text

def validate_cleaned_story(story):
    """Validate story after cleaning"""
    text = story.get('text', '')
    
    # Must have minimum length
    if len(text) < 50:
        return False, "Story too short after cleaning"
    
    # Must have some word content
    words = text.split()
    if len(words) < 20:
        return False, "Too few words after cleaning"
    
    # Check for reasonable character distribution
    alpha_chars = sum(c.isalpha() for c in text)
    if alpha_chars / len(text) < 0.6:
        return False, "Too many non-alphabetic characters"
    
    return True, "OK"

def clean_k5_stories(dry_run=True):
    """Clean all K-5 stories"""
    print("Fetching K-5 stories...")
    response = supabase.table('stories_raw').select('*').in_(
        'grade_level', 
        ['K-1', '2-3', '4-5']
    ).execute()
    
    stories = response.data
    print(f"Found {len(stories)} stories to process\n")
    
    cleaned_count = 0
    skipped_count = 0
    invalid_count = 0
    
    for i, story in enumerate(stories, 1):
        story_id = story.get('story_id')
        title = story.get('title', '')
        original_text = story.get('text', '')
        
        # Clean the text
        cleaned_text = clean_text(original_text, title)
        
        # Check if text was actually changed
        if cleaned_text == original_text:
            skipped_count += 1
            continue
        
        # Validate cleaned story
        story['text'] = cleaned_text
        is_valid, message = validate_cleaned_story(story)
        
        if not is_valid:
            print(f"⚠ [{i}/{len(stories)}] INVALID after cleaning: {title[:50]}")
            print(f"  Reason: {message}")
            invalid_count += 1
            continue
        
        print(f"✓ [{i}/{len(stories)}] Cleaned: {title[:50]}")
        print(f"  Original length: {len(original_text)} chars")
        print(f"  Cleaned length:  {len(cleaned_text)} chars")
        print(f"  Difference:      {len(original_text) - len(cleaned_text)} chars removed")
        
        if not dry_run:
            # Update in database
            supabase.table('stories_raw').update({
                'text': cleaned_text
            }).eq('story_id', story_id).execute()
            print(f"  → Updated in database")
        
        cleaned_count += 1
        print()
    
    print("=" * 70)
    print("CLEANUP SUMMARY")
    print("=" * 70)
    print(f"Total stories processed: {len(stories)}")
    print(f"Stories cleaned:         {cleaned_count}")
    print(f"Stories unchanged:       {skipped_count}")
    print(f"Stories invalid:         {invalid_count}")
    
    if dry_run:
        print("\n⚠ DRY RUN - No changes were made to database")
        print("Run with dry_run=False to apply changes")
    else:
        print("\n✓ Changes saved to database")
    
    return cleaned_count, skipped_count, invalid_count

if __name__ == "__main__":
    import sys
    
    # Default to dry run for safety
    dry_run = True
    
    if len(sys.argv) > 1 and sys.argv[1] == '--apply':
        dry_run = False
        print("⚠ APPLYING CHANGES TO DATABASE\n")
    else:
        print("Running in DRY RUN mode (no changes will be made)")
        print("Use --apply flag to actually update the database\n")
    
    try:
        clean_k5_stories(dry_run=dry_run)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Supabase is running (supabase status)")
        print("  2. Python packages are installed (pip install supabase)")
