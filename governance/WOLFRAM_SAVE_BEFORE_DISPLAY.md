# Wolfram figure generation — save before display

**Status:** normative operational rule for the Computational Difficulty Atlas. Supplements [Visual Production Specification](VISUAL_PRODUCTION_SPEC.md) and [Wolfram Figure Typography](WOLFRAM_FIGURE_TYPOGRAPHY.md).

## Non-negotiable ordering

**Durably save the source and the exact complete exported figure before any display, preview, rasterization, figure-in-chat, browser load, or MkDocs/PDF rendering.** A graphic that appears in a tool response is **not** durable evidence. Rendering large Wolfram figures into a response can crash, truncate, or exhaust output resources.

For each figure:

1. **Source lock first.** Save the complete `.wl` (or notebook) source, generation parameters, figure identifier and caption/claim scope in the Git repository. Commit and push. Record the full commit SHA and verify remote readback. This survives a computation crash.
2. **Generate without display.** Run Wolfram as a bounded file-export operation on an authorized runner (or other filesystem-capable Wolfram environment), e.g. `wolframscript -file figures/src/FXX.wl`. Do not evaluate the graphic as a visual response first. Write a temporary output file, not over a last-known-good artifact.
3. **Validate before promotion.** Parse the complete SVG as XML; check a real `<svg>` root, `viewBox`, vector path geometry, absence of raster image embedding, and figure-specific mathematical claims. Compute content SHA-256 and Git blob SHA. Treat incomplete `ExportString` output, nonmatching fragments, and failed SVG parsing as invalid. Do not infer completeness from a plausible-looking image or balanced tag counts.
4. **Durable exported artifact.** Atomically promote a validated temporary SVG to `figures/generated/`, then commit and push the source and exported artifact to GitHub. Confirm the remote branch/commit tree contains the **exact** bytes and record both blob hashes; include caption/metadata. A short-lived workflow artifact or in-memory Wolfram value is not a substitute for this Git record.
5. **Only then preview.** Preview jobs must checkout that commit and verify the Git blobs **before** loading SVG into any renderer. Inline display is optional. A failed display does not invalidate or destroy the committed output; restore the figure directly from Git on retry.
6. **Review remains separate.** Persistent/valid SVG does not imply theorem correctness, typesetting at final page width, accessibility approval, or publication authority.

## Failure and recovery

- If Wolfram kernel or presentation crashes, preserve the committed source and any last-good, validated exported SVG. Do **not** overwrite good blobs with fragments.
- Restart from the saved commit, with reproducible parameters. Re-export and compare hashes. If output differs, record a new full artifact revision, not a silent overwrite.
- A tool that returns enormous `ExportString` data is a *transport*, not durable storage. Avoid passing that data directly to the conversation renderer. If the only transport is chunked text, reconstruct off-display, check exact byte/character length and full XML parsing, **commit and verify remote readback**, and only then request display. A length check alone is insufficient; chunk boundaries can duplicate or drop quotes.
- If saving or remote verification fails, stop before preview and report the blocker; do not claim that the rendering was archived.

## CI enforcement

`ci/verify_persisted_wolfram_assets.py` ensures each requested figure's Wolfram source, SVG, caption and metadata exist as exact **committed Git blobs** in the checked-out commit. It parses the SVG and writes a small hash/provenance manifest for reviewers. Run it **before** any downstream HTML, SVG-preview, or image-related steps.

This enforcement proves persistence in the checked-out Git tree prior to CI display; it does not prove that historical human/tool actions respected the ordering, nor that a workflow artifact will be retained forever. The durable source of truth is the Git commit/tree.

**Operational invariant:** `SOURCE_COMMITTED -> EXPORT_COMPLETE -> VALIDATED -> EXPORT_COMMITTED_AND_REMOTE_VERIFIED -> PREVIEW -> CRITICAL_REVIEW -> ACCEPTANCE`. No preview may precede committed export.
