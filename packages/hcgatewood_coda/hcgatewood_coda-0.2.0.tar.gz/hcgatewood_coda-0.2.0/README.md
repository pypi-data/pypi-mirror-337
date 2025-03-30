# Coda

Coda is a personal Lodash-style utility library.

## Installation

```bash
pip install hcgatewood_coda
```

## Usage

```python
import coda
```

## Features

- `RateLimiter` basic SQLite-backed sliding window rate limiter
- Env variable loading
    - `must_getenv` get env variable or raise
    - `getenv_bool` get env variable and coerce to bool
