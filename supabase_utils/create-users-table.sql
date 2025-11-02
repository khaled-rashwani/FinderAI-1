-- Table: via-car-user
-- This table stores information about each unique user interacting with the bot.

CREATE TABLE public."via-car-user" (
  user_id BIGINT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  username TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  
  CONSTRAINT "via-car-user_pkey" PRIMARY KEY (user_id)
);

-- Add comments for clarity
COMMENT ON TABLE public."via-car-user" IS 'Stores user data from Telegram.';
COMMENT ON COLUMN public."via-car-user".user_id IS 'Unique Telegram User ID.';