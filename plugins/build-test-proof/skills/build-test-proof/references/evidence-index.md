# One selected final run

Use an index for multi-artifact handoffs, repeated failures/fixes, or an explicitly requested durable report. Keep `FINAL_INDEX.json` in the task's evidence directory. `selected_run` selects a distinct child run directory; final artifact paths are relative to the index and must stay inside that selected run. Keep earlier/before/failed files in other run directories. Different viewport recordings can live inside the selected run with separate scenarios and their actual coverage.

Write only observations from the real run. Required structure:

```json
{
  "schema_version": 1,
  "task": "Website change being checked",
  "run_id": "final-20261012-01",
  "selected_run": "final-20261012-01",
  "source_revision": "actual git SHA or explicit fixture version; disclose if unknown",
  "checked_at": "actual ISO timestamp",
  "environment": { "url": "http://127.0.0.1:43188", "browser": "actual browser and version", "viewport": "1280x800" },
  "skill_activation": { "mode": "catalog_explicit", "evidence": "actual catalog name and loaded entrypoint" },
  "scenarios": [{
    "id": "generated-result",
    "title": "Preview and completed output",
    "status": "passed",
    "actions": "Actual user actions performed",
    "expected": "Expected result",
    "observed": "Observed output",
    "visual_change": true,
    "long_flow": true,
    "screenshots": [{ "path": "final-20261012-01/result.png", "reviewed": true }],
    "video": { "path": "final-20261012-01/flow.webm", "actual_flow": true, "decoded": true, "reviewed": true, "coverage": "Exact recorded steps" },
    "server_result_required": true,
    "server_result": { "status": "passed", "observed": "Actual returned output inspected", "artifacts": ["final-20261012-01/output-receipt.json"] }
  }],
  "unchecked": ["Physical mobile device"]
}
```

Do not use these sample values as evidence. Statuses: `passed`, `failed`, `blocked`, `not_checked`. Activation modes: `catalog_explicit`, `catalog_implicit`, `manual_file`, `unavailable`. For blocked/not_checked, add a precise `limitation`. A visual pass needs a reviewed screenshot; a long-flow pass needs a decoded/reviewed actual-flow recording. If only video is unavailable, split interaction and video coverage into separate scenarios so the interaction may remain passed and the missing video is blocked. A failed actual server result cannot be hidden behind a passed UI scenario marked server-result-required.

Run with existing Python 3.9+:

```sh
python3 /absolute/path/to/skill/scripts/validate-index.py /absolute/task-evidence/FINAL_INDEX.json
```

Exit 0 means structural validity only. Exit 2 identifies broken references, path escape, mixed selected runs or incomplete coverage declarations. The helper never runs a browser, installs dependencies or promotes a failed scenario to passed. File presence, timestamps and declarations do not prove freshness, privacy review, playback or correctness: the agent still has to inspect them and match the code revision. It accepts any nonempty artifact type; decoders and visual inspection remain outside its scope.
