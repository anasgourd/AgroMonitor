# Technical Debt — Post V1

**Status:** Deferred  
**Priority:** Low

### 1. [ ] Backend-Based Alert Acknowledgment

- **Current behavior:** Seen alert IDs are stored in the browser's `localStorage`.
- **Limitation:** Acknowledgment state is browser-specific, does not synchronize across devices, and stored IDs accumulate over time.
- **Future improvement:** Move alert acknowledgment state to the backend and persist it in PostgreSQL.
- **Implementation:** Introduce an acknowledgment field (e.g. `is_acknowledged`) in the Alert model and provide an authenticated API endpoint to update it.
- **Benefit:** Persistent, centralized alert management across browsers and devices.
- **Scope:** Backend, database, and frontend.

### 2. [ ] User Registration (Sign Up Page)

- **Current behavior:** Users can log in, but there is no dedicated frontend registration page.
- **Future improvement:** Implement a Sign Up page using the existing backend registration endpoint.
- **Scope:** Primarily frontend.

### 3. [ ] Dependency Updates

- **Future improvement:** Review and update outdated Python and JavaScript dependencies, prioritizing security-related updates.
- **Validation:** Run backend tests, frontend tests, and production build after updates.
- **Scope:** Backend and frontend.

---

**Decision:** These improvements are deferred and do not block the Software V1 release.