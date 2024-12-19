ALTER TABLE employers
ADD COLUMN employer_uuid VARCHAR(50) NOT NULL AFTER employer_id;

-- Add a unique index to ensure uniqueness of employer_uuid
ALTER TABLE employers
ADD UNIQUE INDEX idx_employer_uuid (employer_uuid);