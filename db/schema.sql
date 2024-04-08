-- Recreating the database if exists
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS queue;

-- Requirements:
-- Adding patient to queue and showing them in order by severity
-- and the time they entered the queue

CREATE TABLE patient (
    patient_id INTEGER PRIMARY KEY,
    name STRING NOT NULL,
    code STRING NOT NULL UNIQUE,
    severity INTEGER NOT NULL CHECK (severity > 0 AND severity < 5)
);

CREATE TABLE patient_queue (
    patient_id INTEGER,
    joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    treated BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    PRIMARY KEY (patient_id)
);
