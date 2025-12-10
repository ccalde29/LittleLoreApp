-- Initial schema from remote database


CREATE TABLE IF NOT EXISTS "public"."stories_raw" (
    "story_id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "source" "text" NOT NULL,
    "nation" "text",
    "title" "text" NOT NULL,
    "text" character varying NOT NULL,
    "region" "text",
    "grade_level" "text",
    "audio_url" "text",
    CONSTRAINT "stories_raw_pkey" PRIMARY KEY ("story_id")
);

CREATE TABLE IF NOT EXISTS "public"."user_profiles" (
    "user_id" "uuid" NOT NULL,
    "grade" "jsonb",
    "preferred_nation" "jsonb",
    "onboarding_complete" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("user_id"),
    CONSTRAINT "user_profiles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id")
);

CREATE TABLE IF NOT EXISTS "public"."user_progress" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "story_id" "uuid" DEFAULT "gen_random_uuid"(),
    "unlocked_words" "text",
    "last_read" timestamp without time zone,
    "completed" timestamp without time zone,
    "completed_at" timestamp without time zone,
    CONSTRAINT "user_progress_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "user_progress_story_id_fkey" FOREIGN KEY ("story_id") REFERENCES "public"."stories_raw"("story_id"),
    CONSTRAINT "user_progress_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."user_profiles"("user_id")
);

-- Enable RLS
ALTER TABLE "public"."stories_raw" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."user_profiles" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."user_progress" ENABLE ROW LEVEL SECURITY;

-- Stories policies
CREATE POLICY "Allow public read access" ON "public"."stories_raw" FOR SELECT USING (true);

-- User profiles policies
CREATE POLICY "Users can view their own profile" ON "public"."user_profiles" FOR SELECT USING (("auth"."uid"() = "user_id"));
CREATE POLICY "Users can update their own profile" ON "public"."user_profiles" FOR UPDATE USING (("auth"."uid"() = "user_id"));
CREATE POLICY "Prevent profile deletion" ON "public"."user_profiles" FOR DELETE USING (false);

-- User progress policies
CREATE POLICY "Users can only see their progress" ON "public"."user_progress" FOR SELECT USING (("auth"."uid"() = "user_id"));
CREATE POLICY "Users can manage own progress" ON "public"."user_progress" TO "authenticated" USING (("auth"."uid"() = "user_id"));
