# Wolfram Figure Typography and Box Geometry

Status: normative amendment to `VISUAL_PRODUCTION_SPEC.md`

Wolfram figures are designed for the size at which they will actually be read on the manuscript page, not for a zoomed standalone export.

## Typography

For a nominal vector width of roughly 720 pt, use these starting tiers:

- principal class/object labels: 20–26 pt;
- primary explanatory text: 16–18 pt;
- relation/status annotations: 15–16 pt;
- minor but essential text: 14 pt minimum.

After manuscript scaling, essential text should ordinarily remain at least about 10.5 pt. If it would become smaller, enlarge the type or redesign the figure.

## Density

If enlarged type does not fit, prefer, in order:

1. shorten the label;
2. wrap it deliberately;
3. enlarge the box or whitespace;
4. move secondary prose to the caption;
5. split the figure.

Do not solve crowding by shrinking essential text below the readability floor.

## Box geometry

No text or symbol may cross, touch, or visually compete with a box boundary, region edge, connector, axis, or grid line.

Boxed text should retain visible clearance on every side, preferably at least 0.5 em and normally closer to 0.75 em at final rendered size.

A connector must stop before a relation label rather than pass through it.

**Boxes are sized to text; text is not shrunk to boxes.**

Any overflow or boundary collision is a figure defect.

## Acceptance

Every Wolfram figure is checked at intended manuscript width, in grayscale, and without zoom. If the figure cannot remain readable and collision-free at that size, simplify or split it.
