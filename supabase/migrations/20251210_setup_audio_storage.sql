-- Create storage bucket for audio files
-- Run this in Supabase SQL Editor or via supabase db push

-- Create the audio bucket if it doesn't exist
INSERT INTO storage.buckets (id, name, public)
VALUES ('audio', 'audio', true)
ON CONFLICT (id) DO NOTHING;

-- Set up storage policies for audio bucket
CREATE POLICY "Public read access for audio files"
ON storage.objects FOR SELECT
USING (bucket_id = 'audio');

CREATE POLICY "Authenticated users can upload audio"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'audio' AND auth.role() = 'authenticated');

CREATE POLICY "Authenticated users can update audio"
ON storage.objects FOR UPDATE
USING (bucket_id = 'audio' AND auth.role() = 'authenticated');

CREATE POLICY "Authenticated users can delete audio"
ON storage.objects FOR DELETE
USING (bucket_id = 'audio' AND auth.role() = 'authenticated');

-- Add index on audio_url for faster queries
CREATE INDEX IF NOT EXISTS idx_stories_audio_url ON stories_raw(audio_url);

-- Add index on grade_level for K-5 filtering
CREATE INDEX IF NOT EXISTS idx_stories_grade_level ON stories_raw(grade_level);

-- Add a function to get stories without audio (for batch processing)
CREATE OR REPLACE FUNCTION get_stories_without_audio(grade_levels text[])
RETURNS TABLE (
    story_id uuid,
    title text,
    text text,
    grade_level text,
    region text,
    nation text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.story_id,
        s.title,
        s.text,
        s.grade_level,
        s.region,
        s.nation
    FROM stories_raw s
    WHERE s.grade_level = ANY(grade_levels)
    AND s.audio_url IS NULL
    ORDER BY s.grade_level, s.title;
END;
$$ LANGUAGE plpgsql;

-- Add a function to get audio generation statistics
CREATE OR REPLACE FUNCTION get_audio_stats()
RETURNS TABLE (
    total_stories bigint,
    stories_with_audio bigint,
    stories_without_audio bigint,
    k1_total bigint,
    k1_with_audio bigint,
    grade_23_total bigint,
    grade_23_with_audio bigint,
    grade_45_total bigint,
    grade_45_with_audio bigint
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_stories,
        COUNT(*) FILTER (WHERE audio_url IS NOT NULL) as stories_with_audio,
        COUNT(*) FILTER (WHERE audio_url IS NULL) as stories_without_audio,
        COUNT(*) FILTER (WHERE grade_level = 'K-1') as k1_total,
        COUNT(*) FILTER (WHERE grade_level = 'K-1' AND audio_url IS NOT NULL) as k1_with_audio,
        COUNT(*) FILTER (WHERE grade_level = '2-3') as grade_23_total,
        COUNT(*) FILTER (WHERE grade_level = '2-3' AND audio_url IS NOT NULL) as grade_23_with_audio,
        COUNT(*) FILTER (WHERE grade_level = '4-5') as grade_45_total,
        COUNT(*) FILTER (WHERE grade_level = '4-5' AND audio_url IS NOT NULL) as grade_45_with_audio
    FROM stories_raw;
END;
$$ LANGUAGE plpgsql;
