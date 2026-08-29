-- Run once in the Supabase SQL editor (Project > SQL Editor) to create the
-- tables SkillRoute's backend expects. The backend always talks to Postgres
-- using the service-role key (see app/utils/supabase_client.py), which
-- bypasses Row Level Security, so RLS is enabled here purely to block any
-- other access path (e.g. the anon/publishable key) from reading this data.

create table if not exists public.profiles (
  user_id text primary key,
  profile jsonb not null,
  updated_at timestamptz not null default now()
);

create table if not exists public.active_roadmaps (
  user_id text primary key,
  career_decision jsonb not null default '{}'::jsonb,
  learning_roadmap jsonb not null default '{}'::jsonb,
  progress jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.career_analyses (
  id uuid primary key default gen_random_uuid(),
  user_id text not null,
  profile jsonb not null,
  career_decision jsonb not null,
  roadmap jsonb not null,
  created_at timestamptz not null default now()
);
create index if not exists career_analyses_user_id_idx on public.career_analyses (user_id);

alter table public.profiles enable row level security;
alter table public.active_roadmaps enable row level security;
alter table public.career_analyses enable row level security;
