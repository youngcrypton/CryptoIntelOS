# Query API Contracts

Framework-neutral contracts define `POST /query`, `POST /search`, `GET /query/{id}`, and `GET /query/statistics`. `QueryRequest`, `SearchRequest`, response contracts, and route metadata contain no web-framework dependency. Authentication, persistence, and HTTP serialization belong to the future API product layer.

CLI equivalents are `cryptointel query`, `cryptointel search`, and `cryptointel explain-query`, with JSON data, pretty output, trace, and statistics flags.
