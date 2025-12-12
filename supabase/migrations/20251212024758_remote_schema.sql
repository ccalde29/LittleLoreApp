drop extension if exists "pg_net";


  create table "public"."stories_raw" (
    "story_id" uuid not null default gen_random_uuid(),
    "source" text not null,
    "nation" text,
    "title" text not null,
    "text" character varying not null,
    "region" text,
    "grade_level" text,
    "audio_url" text
      );


alter table "public"."stories_raw" enable row level security;


  create table "public"."user_profiles" (
    "user_id" uuid not null,
    "grade" jsonb,
    "preferred_nation" jsonb,
    "onboarding_complete" boolean default false,
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now()
      );


alter table "public"."user_profiles" enable row level security;


  create table "public"."user_progress" (
    "id" uuid not null default gen_random_uuid(),
    "user_id" uuid not null default gen_random_uuid(),
    "story_id" uuid default gen_random_uuid(),
    "unlocked_words" text,
    "last_read" timestamp without time zone,
    "completed" timestamp without time zone,
    "completed_at" timestamp without time zone
      );


alter table "public"."user_progress" enable row level security;

CREATE UNIQUE INDEX stories_raw_pkey ON public.stories_raw USING btree (story_id);

CREATE UNIQUE INDEX user_profiles_pkey ON public.user_profiles USING btree (user_id);

CREATE UNIQUE INDEX user_progress_pkey ON public.user_progress USING btree (id);

alter table "public"."stories_raw" add constraint "stories_raw_pkey" PRIMARY KEY using index "stories_raw_pkey";

alter table "public"."user_profiles" add constraint "user_profiles_pkey" PRIMARY KEY using index "user_profiles_pkey";

alter table "public"."user_progress" add constraint "user_progress_pkey" PRIMARY KEY using index "user_progress_pkey";

alter table "public"."user_profiles" add constraint "user_profiles_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."user_profiles" validate constraint "user_profiles_user_id_fkey";

alter table "public"."user_progress" add constraint "user_progress_story_id_fkey" FOREIGN KEY (story_id) REFERENCES public.stories_raw(story_id) not valid;

alter table "public"."user_progress" validate constraint "user_progress_story_id_fkey";

alter table "public"."user_progress" add constraint "user_progress_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.user_profiles(user_id) not valid;

alter table "public"."user_progress" validate constraint "user_progress_user_id_fkey";

grant delete on table "public"."stories_raw" to "anon";

grant insert on table "public"."stories_raw" to "anon";

grant references on table "public"."stories_raw" to "anon";

grant select on table "public"."stories_raw" to "anon";

grant trigger on table "public"."stories_raw" to "anon";

grant truncate on table "public"."stories_raw" to "anon";

grant update on table "public"."stories_raw" to "anon";

grant delete on table "public"."stories_raw" to "authenticated";

grant insert on table "public"."stories_raw" to "authenticated";

grant references on table "public"."stories_raw" to "authenticated";

grant select on table "public"."stories_raw" to "authenticated";

grant trigger on table "public"."stories_raw" to "authenticated";

grant truncate on table "public"."stories_raw" to "authenticated";

grant update on table "public"."stories_raw" to "authenticated";

grant delete on table "public"."stories_raw" to "service_role";

grant insert on table "public"."stories_raw" to "service_role";

grant references on table "public"."stories_raw" to "service_role";

grant select on table "public"."stories_raw" to "service_role";

grant trigger on table "public"."stories_raw" to "service_role";

grant truncate on table "public"."stories_raw" to "service_role";

grant update on table "public"."stories_raw" to "service_role";

grant delete on table "public"."user_profiles" to "anon";

grant insert on table "public"."user_profiles" to "anon";

grant references on table "public"."user_profiles" to "anon";

grant select on table "public"."user_profiles" to "anon";

grant trigger on table "public"."user_profiles" to "anon";

grant truncate on table "public"."user_profiles" to "anon";

grant update on table "public"."user_profiles" to "anon";

grant delete on table "public"."user_profiles" to "authenticated";

grant insert on table "public"."user_profiles" to "authenticated";

grant references on table "public"."user_profiles" to "authenticated";

grant select on table "public"."user_profiles" to "authenticated";

grant trigger on table "public"."user_profiles" to "authenticated";

grant truncate on table "public"."user_profiles" to "authenticated";

grant update on table "public"."user_profiles" to "authenticated";

grant delete on table "public"."user_profiles" to "service_role";

grant insert on table "public"."user_profiles" to "service_role";

grant references on table "public"."user_profiles" to "service_role";

grant select on table "public"."user_profiles" to "service_role";

grant trigger on table "public"."user_profiles" to "service_role";

grant truncate on table "public"."user_profiles" to "service_role";

grant update on table "public"."user_profiles" to "service_role";

grant delete on table "public"."user_progress" to "anon";

grant insert on table "public"."user_progress" to "anon";

grant references on table "public"."user_progress" to "anon";

grant select on table "public"."user_progress" to "anon";

grant trigger on table "public"."user_progress" to "anon";

grant truncate on table "public"."user_progress" to "anon";

grant update on table "public"."user_progress" to "anon";

grant delete on table "public"."user_progress" to "authenticated";

grant insert on table "public"."user_progress" to "authenticated";

grant references on table "public"."user_progress" to "authenticated";

grant select on table "public"."user_progress" to "authenticated";

grant trigger on table "public"."user_progress" to "authenticated";

grant truncate on table "public"."user_progress" to "authenticated";

grant update on table "public"."user_progress" to "authenticated";

grant delete on table "public"."user_progress" to "service_role";

grant insert on table "public"."user_progress" to "service_role";

grant references on table "public"."user_progress" to "service_role";

grant select on table "public"."user_progress" to "service_role";

grant trigger on table "public"."user_progress" to "service_role";

grant truncate on table "public"."user_progress" to "service_role";

grant update on table "public"."user_progress" to "service_role";


  create policy "Allow public read access"
  on "public"."stories_raw"
  as permissive
  for select
  to public
using (true);



  create policy "Anyone can read stories"
  on "public"."stories_raw"
  as permissive
  for select
  to authenticated
using (true);



  create policy "Prevent profile deletion"
  on "public"."user_profiles"
  as permissive
  for delete
  to public
using (false);



  create policy "User can manage their profile"
  on "public"."user_profiles"
  as permissive
  for all
  to public
using ((auth.uid() = user_id));



  create policy "Users can manage own profile"
  on "public"."user_profiles"
  as permissive
  for all
  to authenticated
using ((auth.uid() = user_id));



  create policy "Users can update their own profile"
  on "public"."user_profiles"
  as permissive
  for update
  to public
using ((auth.uid() = user_id));



  create policy "Users can view their own profile"
  on "public"."user_profiles"
  as permissive
  for select
  to public
using ((auth.uid() = user_id));



  create policy "Users can manage own progress"
  on "public"."user_progress"
  as permissive
  for all
  to authenticated
using ((auth.uid() = user_id));



  create policy "Users can only see their progress"
  on "public"."user_progress"
  as permissive
  for select
  to public
using ((auth.uid() = user_id));



