-- ============================================================
-- SkillRoute — Supabase Migration
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- 0. Enable UUID generation
create extension if not exists "uuid-ossp";

-- ============================================================
-- 1. USERS TABLE
-- Stores student profile data. Row ID matches the Supabase
-- Auth user ID so auth.uid() can be used in RLS policies.
-- ============================================================
create table if not exists users (
  id         uuid primary key references auth.users(id) on delete cascade,
  profile    jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Index for fast lookups by user ID (already PK, but explicit)
create index if not exists idx_users_updated_at on users (updated_at desc);

comment on table  users            is 'Student profiles — one row per Supabase Auth user';
comment on column users.id         is 'Matches auth.users.id (Supabase Auth UID)';
comment on column users.profile    is 'JSON blob: name, education, skills, interests, goals, etc.';
comment on column users.updated_at is 'Last profile update timestamp';

-- ============================================================
-- 2. ROADMAPS TABLE
-- Stores the active career roadmap + progress for each user.
-- One row per user (upserted on save).
-- ============================================================
create table if not exists roadmaps (
  id               uuid primary key default uuid_generate_v4(),
  user_id          uuid not null unique references auth.users(id) on delete cascade,
  career_decision  jsonb not null default '{}'::jsonb,
  learning_roadmap jsonb not null default '{}'::jsonb,
  progress         jsonb not null default '{"completed_phases":0,"total_phases":0,"streak_days":0,"last_activity_date":null}'::jsonb,
  updated_at       timestamptz not null default now()
);

create index if not exists idx_roadmaps_user_id   on roadmaps (user_id);
create index if not exists idx_roadmaps_updated_at on roadmaps (updated_at desc);

comment on table  roadmaps               is 'Active learning roadmap + progress — one row per user';
comment on column roadmaps.user_id       is 'FK to auth.users (unique — one roadmap per user)';
comment on column roadmaps.career_decision is 'AI-generated career match + confidence scores';
comment on column roadmaps.learning_roadmap is 'Full roadmap JSON (phases, skills, milestones)';
comment on column roadmaps.progress      is 'Completion count, streak, last activity';

-- ============================================================
-- 3. ANALYSES TABLE
-- History of every roadmap generation (append-only log).
-- ============================================================
create table if not exists analyses (
  id               uuid primary key default uuid_generate_v4(),
  user_id          uuid not null references auth.users(id) on delete cascade,
  profile          jsonb not null default '{}'::jsonb,
  career_decision  jsonb not null default '{}'::jsonb,
  roadmap          jsonb not null default '{}'::jsonb,
  created_at       timestamptz not null default now()
);

create index if not exists idx_analyses_user_id    on analyses (user_id);
create index if not exists idx_analyses_created_at on analyses (created_at desc);

comment on table  analyses      is 'Historical log of every roadmap generation per user';
comment on column analyses.user_id is 'FK to auth.users';

-- ============================================================
-- 4. ROW-LEVEL SECURITY (RLS)
-- Users can only read/write their own data.
-- The service_role key (used by the backend) bypasses RLS.
-- ============================================================

alter table users    enable row level security;
alter table roadmaps enable row level security;
alter table analyses enable row level security;

-- ── USERS policies ──────────────────────────────────────────
-- Read own profile
create policy "Users can read own profile"
  on users for select
  using (auth.uid() = id);

-- Insert own profile (first signup)
create policy "Users can insert own profile"
  on users for insert
  with check (auth.uid() = id);

-- Update own profile
create policy "Users can update own profile"
  on users for update
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- ── ROADMAPS policies ───────────────────────────────────────
-- Read own roadmap
create policy "Users can read own roadmap"
  on roadmaps for select
  using (auth.uid() = user_id);

-- Insert own roadmap
create policy "Users can insert own roadmap"
  on roadmaps for insert
  with check (auth.uid() = user_id);

-- Update own roadmap
create policy "Users can update own roadmap"
  on roadmaps for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- Delete own roadmap (reset)
create policy "Users can delete own roadmap"
  on roadmaps for delete
  using (auth.uid() = user_id);

-- ── ANALYSES policies ───────────────────────────────────────
-- Read own analyses
create policy "Users can read own analyses"
  on analyses for select
  using (auth.uid() = user_id);

-- Insert own analyses
create policy "Users can insert own analyses"
  on analyses for insert
  with check (auth.uid() = user_id);

-- ============================================================
-- 5. UPDATED_AT TRIGGER
-- Automatically set updated_at on every write.
-- ============================================================
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger set_users_updated_at
  before update on users
  for each row execute function update_updated_at();

create trigger set_roadmaps_updated_at
  before update on roadmaps
  for each row execute function update_updated_at();

-- ============================================================
-- 6. ENABLE REALTIME (optional — for live dashboard updates)
-- ============================================================
alter publication supabase_realtime add table roadmaps;
alter publication supabase_realtime add table users;

-- ============================================================
-- DONE — All tables, indexes, RLS, and triggers are in place.
--
-- The backend uses the SERVICE_ROLE key (SUPABASE_SERVICE_KEY)
-- which bypasses RLS, so all backend routes work without
-- requiring per-user RLS policy matching.
--
-- Frontend browser queries (if any) will be restricted to
-- the user's own rows by RLS.
-- ============================================================
