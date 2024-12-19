ALTER TABLE users
ADD COLUMN user_uuid VARCHAR(50) NOT NULL AFTER user_id;

-- Add a unique index to ensure uniqueness of user_uuid
ALTER TABLE users
ADD UNIQUE INDEX idx_user_uuid (user_uuid);