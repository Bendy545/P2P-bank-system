# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project initialization and base repository setup (Author: Bendy545)
- MIT License added to the project (Author: Martin Chmelík)
- DAO layer and database initialization script `database.sql` (Author: Bendy545)
- TCP server and command set implementation (Author: Bendy545)
- Application layer added with commands (Author: Bendy545)
- Application architecture diagram (Author: Bendy545)
- Custom library and codebase refactoring to use it (Author: Bendy545)
- Database logging functionality (Author: Bendy545)
- SQLite fallback in case of MySQL connection failure (Author: Bendy545)
- Project documentation in `README.md` (Author: Bendy545)
- `CHANGELOG.md` file added (Author: Sofia)

### Changed

- Database system switched from Oracle to MySQL (Author: Bendy545)
- Transition from `threading` to true parallel processing using `multiprocessing` (Author: Bendy545)
- Application architecture redesign (Author: Bendy545)

### Fixed

- TCP server fixes and command import corrections (Author: Bendy545)
- Thread-safe database access implementation (Author: Bendy545)
