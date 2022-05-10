CREATE TABLE IF NOT EXISTS runs (
  id serial primary key,
  name text NOT NULL,
  start_at bigint,
  end_at bigint,
  status int default 0
);
