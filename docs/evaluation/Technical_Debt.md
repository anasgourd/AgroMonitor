# Technical Debt — Post V1

**Status:** Deferred  
**Priority:** Low–Medium

### 1. [ ] Backend-Based Alert Acknowledgment & Database Migrations

- **Current behavior:** Seen alert IDs are stored in the browser's `localStorage`. Database schema changes are not managed through versioned migrations.
- **Limitation:** Acknowledgment state is browser-specific, does not synchronize across devices, and stored IDs accumulate over time. Database schema changes also require manual management.
- **Future improvement:** Move alert acknowledgment state to the backend, persist it in PostgreSQL, and introduce Alembic for database schema migrations.
- **Implementation:**
  - Add an `is_acknowledged` field to the Alert model.
  - Introduce Alembic to manage database schema changes.
  - Create a migration for the new column.
  - Provide an authenticated API endpoint to update acknowledgment status.
  - Update the frontend to use backend acknowledgment state.
- **Benefit:** Persistent, centralized alert management across devices and controlled database schema evolution.
- **Scope:** Backend, database, and frontend.
- **Priority:** Low–Medium.

### 2. [ ] Dependency Updates

- **Current behavior:** The application uses the Python and JavaScript dependencies selected during V1 development.
- **Limitation:** Dependencies may become outdated over time, potentially introducing security, compatibility, or maintenance concerns.
- **Future improvement:** Periodically review and update outdated dependencies, prioritizing security-related updates.
- **Validation:** Run backend tests, frontend tests (where available), and the frontend production build after updates.
- **Scope:** Backend and frontend.
- **Priority:** Low.

---

**Decision:** These improvements are deferred and do not block the AgroMonitor Software V1 release. They are documented for future maintenance and development.

