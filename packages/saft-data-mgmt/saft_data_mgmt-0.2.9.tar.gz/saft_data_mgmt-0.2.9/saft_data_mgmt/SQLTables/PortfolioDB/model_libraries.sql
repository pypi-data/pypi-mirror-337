CREATE TABLE IF NOT EXISTS ModelLibraries (
    model_library_id INTEGER PRIMARY KEY,
    model_library TEXT NOT NULL,
    UNIQUE (model_library)
);