CREATE TABLE IF NOT EXISTS FuturesMetadata (
    [symbol_id] INTEGER PRIMARY KEY,
    [exchange_id] INTEGER,
    [multiplier] REAL,
    [min_tick_size] REAL,
    [min_tick_value] REAL,
    [underlying_asset_type_id] INTEGER,
    [underlying_asset_name] TEXT,
    UNIQUE (symbol_id),
    FOREIGN KEY (underlying_asset_type_id)
        REFERENCES UnderlyingAssetTypes(underlying_asset_type_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
);