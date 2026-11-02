-- OPTIONAL DEMO SETUP. Read the privacy/security notes in README.md.
-- Anonymous insert/read is NOT suitable for a trusted graded competition.
create table if not exists public.math_scores (
  id bigint generated always as identity primary key,
  name text not null check (char_length(trim(name)) between 1 and 24),
  score integer not null check (score between 0 and 9999999),
  level integer not null check (level between 1 and 3),
  correct integer not null check (correct between 0 and 9999),
  wrong integer not null check (wrong between 0 and 9999),
  accuracy integer not null check (accuracy between 0 and 100),
  best_combo integer not null check (best_combo between 0 and 9999),
  date timestamptz not null default now()
);
create index if not exists math_scores_score_idx on public.math_scores (score desc);
alter table public.math_scores enable row level security;

-- For classroom prototype only. Consider authenticated per-class access and server score checks.
drop policy if exists "read scores demo" on public.math_scores;
create policy "read scores demo" on public.math_scores for select to anon using (true);
drop policy if exists "insert scores demo" on public.math_scores;
create policy "insert scores demo" on public.math_scores for insert to anon
with check (char_length(trim(name)) between 1 and 24 and score between 0 and 9999999
  and level between 1 and 3 and accuracy between 0 and 100);
-- There are intentionally no update/delete policies for anon users.
grant usage on schema public to anon;
grant select, insert on public.math_scores to anon;
