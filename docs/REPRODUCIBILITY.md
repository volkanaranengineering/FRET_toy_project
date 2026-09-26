# Reproduction guide

## Reproduction levels

1. **Archive verification:** Python checks file hashes, counts, formulas, recorded outcomes, local links and raw HTTP hashes. No FRET/MATLAB execution.
2. **Fresh examples:** Python standard library and Node regenerate local HTTP observations and schedule snapshots, then run the authored subset checker.
3. **Fresh FRET compilation:** Node 20.19.0, npm and the committed FRET lockfile.
4. **Native desktop:** additional app dependencies, Electron runtime and build. Optional analysis backends remain separate.
5. **Historical research:** archived MATLAB/paper workflows need their own external tools and some original path adaptations.

## Read results

```sh
python tools/verify_archive.py
python -m http.server 8766 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8766/projects/index.html`, or open the HTML directly. GitHub Pages is not configured. Stop the server with Ctrl+C.

## Compiler setup

From the repository root, using Node 20.19.0:

```sh
npm ci --prefix vendor/fret/fret-electron --ignore-scripts --legacy-peer-deps --no-audit --no-fund
```

Or PowerShell: `./tools/setup-fret.ps1`.

The upstream lockfile fixes dependency versions. Ignoring lifecycle scripts avoids the upstream Unix-oriented installer and suffices for headless compilation. This source snapshot uses older research dependencies; upgrading them changes the baseline and should be reviewed separately.

## Fresh compilation and observations

```sh
node projects/build.cjs
python projects/collect-evidence.py
node projects/check-examples.cjs
node projects/report.cjs
python tools/verify_archive.py
```

PowerShell wrapper: `./tools/reproduce.ps1 -Python python`.

Expected: 10 projects, 61 requirements, zero parse errors, 40 HTTP requests, 20 pairs, 30 snapshots, 177 matching outcomes. The HTTP server binds only to localhost on an ephemeral port; no external requests are made by the experiment. Collection uses the included `research/revision_v3/artifact/http_case.py` and `research/decision_workflows/ledger_schedules.py`. New outputs go to `projects/`, leaving archived research results intact.

Changing inputs can change manifest hashes. Review changes before deliberately running `python tools/catalog_archive.py` to record a new baseline; do not refresh merely to hide unexpected mismatches.

## Existing FRET installation

```powershell
$env:FRET_HOME = 'C:\path\to\fret\fret-electron'
node projects/build.cjs
```

That directory must contain the compiler and installed dependencies. Unset the variable to use the vendored snapshot. The compiler hash is recorded in `projects/compilation-summary.json`.

## Windows desktop

```powershell
./tools/setup-fret.ps1 -Desktop
node projects/seed-database.cjs
./projects/Show-Toy-Projects.cmd
```

Desktop setup installs locked app and LTLSIM JavaScript-library dependencies, explicitly installs Electron, then runs the upstream build. It does not install NuSMV, LTLSIM native binaries, JKind, Kind2 or Z3. See the vendored upstream README for other platform/setup routes. The compiler/examples were rerun in this repository; the optional full desktop rebuild recipe is based on the original installation and has not been rerun here.

The seed command initializes only `projects/desktop-data/fret-db` and refuses to overwrite a nonempty database. The launcher uses that dedicated database and profile; neither is committed. After a rebuild, import updated JSON through FRET and review duplicate/conflict handling rather than rerunning the initializer.

Alternatively open an installed FRET and import `projects/all-projects.json`. All names are preserved. Prefer JSON: the upstream CSV path may quote descriptions as unformalized free text. Configure variable types/model mappings from project signal dictionaries before external verification export; no completed external mappings are claimed.

## Tutorial

`node tutorial/prepare-example.cjs` regenerates the two original tutorial specifications. The PDF and screenshots preserve the original application run. `tutorial/build_tutorial.py` can regenerate the PDF with ReportLab and Windows Arial fonts; it is not part of the verified headless workflow.

## Archived research

`research/revision_v3/artifact/` contains the earlier record-contract experiment, HTTP server, trajectory, MATLAB verification and data. Its paper reports its own study counts, distinct from the 177 FRET example checks.

The door/six-level reports and `research/matlab/` preserve the visualization lineage. Some original scripts retain machine-specific output paths. They are archival context, not portable FRET setup scripts. MATLAB, LaTeX and commercial fonts are external dependencies.
