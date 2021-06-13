-- Database schema for Flask app 'cole'.

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  -- Don't currently care - just want to store all/most visits of UUID #N so we can do daily, monthly, etc. active users.
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  -- No 'uuid' type - use blob so we can store as 16 bytes instead of string (36(?) bytes).
  uuid BLOB NOT NULL,
  -- Does TIMESTAMP work as a datatype for sqlite3?
  -- Docs don't have it but tutorial I'm riffing off of does use it for the sqlite3 db.
  -- And it doesn't like the unix timestamps I'm inserting, so... replace with INTEGER.
  visited_at INTEGER NOT NULL
);
