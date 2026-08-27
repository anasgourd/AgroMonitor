# AgroMonitor

AgroMonitor is a React web application for monitoring agricultural fields, viewing sensor-based metrics, and reviewing field-level status at a glance.

## Development

```bash
npm install
npm run dev
```

## Non-Functional Requirements (NFRs)

1. **Performance**
   - The dashboard should render the initial view in under 2 seconds on a standard broadband connection and a modern desktop browser.
   - Navigation between the field list and field dashboard should complete in under 500 ms.

2. **Availability & Reliability**
   - The deployed application should target 99.5% monthly uptime.
   - Failures in loading field data should present a user-facing fallback state rather than a blank screen.

3. **Usability**
   - Core workflows (viewing fields and opening a field dashboard) should be usable on mobile, tablet, and desktop screen sizes.
   - Text and controls should maintain accessible contrast and readable sizing for default browser zoom.

4. **Maintainability**
   - All pull requests must pass lint checks (`npm run lint`) before merge.
   - UI behavior should remain componentized and reusable (e.g., shared cards and page components) to reduce duplication.

5. **Security & Privacy**
   - No secrets (API keys, tokens, credentials) may be committed to the repository.
   - Any future backend/API integration must use HTTPS for data in transit.
