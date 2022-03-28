CREATE TABLE IF NOT EXISTS metadata (
   hash VARCHAR PRIMARY KEY,
   name VARCHAR NOT NULL, -- 'i.e. lectures, lecture01.mov'
   type VARCHAR NOT NULL, -- 'file' or 'directory'
   file_extension VARCHAR, -- 'i.e. .pdf, .doc, .py'
   media_format VARCHAR, -- 'audio, video, notes'
   upload_timestamp timestamp NOT NULL,
   bytesize INT NOT NULL,
   tags VARCHAR[],
   uploaded_by VARCHAR
);
