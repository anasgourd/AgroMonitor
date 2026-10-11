**Technical Debt: Seen Alerts Local Storage Cleanup**

- **Current behavior:** Seen alert IDs αποθηκεύονται στο browser `localStorage` και παραμένουν εκεί, ώστε τα επιβεβαιωμένα alerts να μην εμφανίζονται ξανά μετά από refresh.
- **Limitation:** Τα IDs συσσωρεύονται καθώς δημιουργούνται και επιβεβαιώνονται νέα alerts.
- **Impact:** Μικρό για το V1, καθώς τα IDs καταλαμβάνουν ελάχιστο χώρο.
- **Future improvement:** Καθαρισμός των Seen IDs όταν τα αντίστοιχα alerts διαγράφονται από το backend, ώστε να διατηρούνται μόνο οι απαραίτητες εγγραφές.
- **Scope:** Frontend improvement, χωρίς απαραίτητη αλλαγή στο backend API.
- **Priority:** Low — να αντιμετωπιστεί όταν χρειαστεί βελτίωση της διαχείρισης των alerts.