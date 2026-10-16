**Technical Debt: Seen Alerts Local Storage Cleanup**

- **Current behavior:** Seen alert IDs αποθηκεύονται στο browser `localStorage` και παραμένουν εκεί, ώστε τα επιβεβαιωμένα alerts να μην εμφανίζονται ξανά μετά από refresh.
- **Limitation:** Τα IDs συσσωρεύονται καθώς δημιουργούνται και επιβεβαιώνονται νέα alerts.
- **Impact:** Μικρό για το V1, καθώς τα IDs καταλαμβάνουν ελάχιστο χώρο.
- **Future improvement:** Καθαρισμός των Seen IDs όταν τα αντίστοιχα alerts διαγράφονται από το backend, ώστε να διατηρούνται μόνο οι απαραίτητες εγγραφές.
- **Scope:** Frontend improvement, χωρίς απαραίτητη αλλαγή στο backend API.
- **Priority:** Low — να αντιμετωπιστεί όταν χρειαστεί βελτίωση της διαχείρισης των alerts.

### [ ] Improve Backend Test Coverage Before V1 Release

**Current status:** All tests passing, 93% backend coverage.

Before the V1 release, review uncovered error-handling and edge-case branches and add tests where they provide meaningful coverage.

- [ ] **Security:** Test invalid, expired and malformed JWTs, including missing required claims.
- [ ] **API routers:** Cover remaining error paths, such as `404 Not Found`, authentication failures and ownership violations.
- [ ] **Repositories:** Test missing resources and failure cases (e.g. returning `False` when a field does not exist).
- [ ] **Services:** Test business-rule violations, including inactive sensors, missing sensors and future measurement timestamps.
- [ ] **Final verification:** Run the complete test suite with coverage, review failures and regressions, and confirm the final coverage report before release.

**Priority:** Before V1 release  
