# Refactoring Plan: Database Concurrency and App Structure

This plan outlines the steps to address critical database connection issues, implement the Application Factory pattern, and improve code consistency in the `m3_2hw` project.

## 1. Database Refactoring (Connection Pooling)

- **Problem**: The current global connection is not thread-safe and can cause issues under concurrent load.
- **Solution**: Replace the single connection in `connect_db.py` with `psycopg2.pool.ThreadedConnectionPool`.
- **Implementation**:
  - Initialize a global pool instance.
  - Provide a method to acquire and release connections from the pool.

## 2. Connection Lifecycle Management

- **Strategy**: Per-request connection handling using Flask's `g` object.
- **Details**:
  - `get_db()` helper to retrieve a connection from the pool and store it in `g.db`.
  - `@app.teardown_appcontext` to ensure the connection is returned to the pool, regardless of success or failure.
  - **Explicit Commits**: Each route will be responsible for calling `g.db.commit()` when performing write operations (even for SELECTs as requested for control).

## 3. Application Factory Pattern

- **Structure**:
  - Move logic from the global scope of `app.py` into a `create_app()` function.
  - Use Flask Blueprints to organize routes.
  - Initialize the database pool within the factory or a dedicated initialization function.

## 4. Type Hints Consistency

- **Task**: Update all route functions to have consistent return type hints.
- **Types**: Use `flask.typing.ResponseReturnValue` or specific types like `str | tuple[str, int]`.

## 5. Constraints

- **Dead Code**: Do NOT remove any commented-out code (lines starting with `#` or block comments).
- **Environment**: Keep using `0.0.0.0:8082` for development.

## Steps

1. Refactor `connect_db.py` to implement `ThreadedConnectionPool`.
2. Update `app.py` to implement `create_app()` and use Blueprints for routes.
3. Integrate `g` and `teardown_appcontext` for database connection management.
4. Apply consistent type hinting to all functions.
5. Verify changes by running the app and checking connectivity.
