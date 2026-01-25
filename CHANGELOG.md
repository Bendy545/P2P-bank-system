# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - 2026-01-25

### Added

- Simple user interface for monitoring the node's status and operation (Author: Sofia Hennelová)
  - Provides a graphical overview of node status, including bank code, ports, command timeout, client count, server running state, and database backend.
  - Allows safe shutdown of the node.
  - Shows last logs (Author: Martin Chmelík)
- TCP server now supports safe shutdown via the monitor interface (Author: Sofia Hennelová)
- exe file added (Author: Martin Chmelík)

### Changed
- Database tables initialization on startup of the program. (Author: Martin Chmelík)
  - No need for the user to create tables, now he only needs to create database user and the database
- DATABASE.sql. (Author: Martin Chmelík)
  - deleted creating the database and also the start transaction statement.

### Fixed
- Process handling when opening monitor and after connecting through putty. (Author: Martin Chmelík)
- Showing last logs - MySQL (Author: Sofia Hennelová)

## [v1.0.0] - 2026-01-20

### Added

- Project initialization and base repository setup (Author: Martin Chmelík)
- MIT License added to the project (Author: Martin Chmelík)
- DAO layer and database initialization script `database.sql` (Author: Martin Chmelík)
- TCP server and command set implementation (Author: Martin Chmelík)
- Application layer added with commands (Author: Martin Chmelík)
- Application architecture diagram (Author: Martin Chmelík)
- Custom library and codebase refactoring to use it (Author: Martin Chmelík)
- Database logging functionality (Author: Martin Chmelík)
- SQLite fallback in case of MySQL connection failure (Author: Martin Chmelík)
- Project documentation in `README.md` (Author: Martin Chmelík)

### Changed

- Database system switched from Oracle to MySQL (Author: Martin Chmelík)
- Transition from `threading` to true parallel processing using `multiprocessing` (Author: Martin Chmelík)
- Application architecture redesign (Author: Martin Chmelík)

### Fixed

- TCP server fixes and command import corrections (Author: Martin Chmelík)
- Thread-safe database access implementation (Author: Martin Chmelík)
