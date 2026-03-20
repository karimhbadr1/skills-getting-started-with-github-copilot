## Plan: Add FastAPI backend tests in tests/ directory

TL;DR - Add pytest support to requirements, create tests directory, and write decently strong coverage for activities API in src/app.py with isolated, reproducible tests.

Steps
1. Confirm current API surface in src/app.py.
   - GET /activities and GET / (redirect), POST /activities/{activity}/signup, DELETE /activities/{activity}/participants
   - In-memory activities store is global mutable state.
2. Add pytest to dependencies.
   - Edit requirements.txt: include pytest (or add `pytest` line if missing).
3. Create tests directory structure.
   - `tests/` at repository root.
4. Create `tests/test_app.py` with TestClient from fastapi.
   - import `TestClient` from fastapi.testclient.
   - import `app`, `activities` (global dict) from `src.app`.
   - define `reset_activities()` helper to restore base dataset in each test.
   - optional pytest fixture `@pytest.fixture(autouse=True)` to reset before each test.
5. Write tests following AAA pattern:
   - `test_get_activities_returns_initial_data`: GET /activities returns 200 with keys and participants arrays.
   - `test_signup_for_activity_adds_participant`: signup new email to existing activity and assert 200 + participant appears in GET.
   - `test_signup_duplicate_participant`: if API currently allows duplicates, assert there is no duplicate handling (or adjust app to reject duplicates as bugfix plus test). If we already added duplicate guard, assert 400.
   - `test_remove_participant`: remove an existing participant with DELETE and check participant removed.
   - `test_remove_nonexistent_participant_returns_404`: delete unknown participant returns 404 and no changes.
   - `test_remove_activity_not_found_returns_404`.
6. Run tests locally.
   - `pytest -q` and ensure 5+ tests pass.
7. Optionally enhance tests for UI behavior not needed now.

Relevant files
- `requirements.txt`
- `src/app.py`
- `tests/test_app.py` (new file)

Verification
1. Run `pytest -q`, verify all tests pass.
2. Confirm no global state leak (all tests independent) by checking same setup function resets activities.
3. Optional: run `uvicorn src.app:app --reload` and `curl` or Postman calls to exercise same behavior manually.

Decisions
- Use tests directory root (`tests/`) as requested.
- Keep tests backend-only; no frontend DOM tests.
- If code already forbids duplicates, test for it; if code allows, adjust app to new behavior and tests accordingly.

Further Considerations
1. If using the low-level shared dict in process scope, resetting contents is needed in each test to avoid flakiness.
2. Ensure `pytest.ini` environment is already configured, no changes required unless needed.
3. Could add pre-commit lint/test workflow in GitHub actions after this change.
