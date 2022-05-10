CREATE TABLE IF NOT EXISTS jobs (
  id serial primary key,
  name text NOT NULL,
  start_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  end_at timestamp with time zone,
  status int default 0
);
