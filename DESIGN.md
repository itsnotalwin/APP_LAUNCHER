# Design — Launchpad (editorial monochrome)

Approved direction: user's reference image (monochrome editorial app). Mode: Operate.

## Color
Light default: paper #ffffff, ink #0b0b0b, mist #efefef, hairline #d9d9d9, muted text #4a4a4a. Dark inverts: #0b0b0b / #f4f4f4 / #1b1b1b / #2e2e2e / #b4b4b4. No accent colour; emphasis is ink fills.

## Type
Source Serif 4 700 for masthead, headings, repo names. Hanken Grotesk 300-500 for body and labels. Small caps labels: 11px, +.14em tracking. Heading scale: 76 / 22 / 20.

## Material
Blobs are original procedural artwork (assets/generate_blobs.py): smooth asymmetric spline silhouettes with a concave shoulder, filled with distressed charcoal (mottle, grain, dust, short scratches) like the reference. Two silhouettes: hero and detail. Dark theme inverts them to chalk-white. Pale organic flat shapes sit behind; dashed slash field (not stripes) and dot grid overlap. Used in the hero, detail header and app icons only. Every raster carries embedded provenance.

## Components
Index rows with hairlines that invert on hover; inverted first "recent" card; pill filter chips; text-underline toggles; square commit markers on a hairline timeline; 52px ink "Launch site" button, radius 8px.

## Motion
Thesis: ink. Things fill, flood and settle; nothing bounces. Ease-out-expo, 200-500ms, transform/opacity/clip-path only.
Focal moment: theme toggle floods the page with ink in a circle from the button (View Transition, clip-path).
Continuity: repo name morphs from its row to the detail title and back (scroll restored); filter/sort reorder rows by shared-element transition; branch underline travels between tabs; commit details open by height.
Feedback: rows fill black from the left on hover and drain right; underlines draw on tabs and search focus; launch arrow slides through; pressed states on rows, chips, buttons.
Reduced motion or no View Transitions API: instant swaps, colour feedback kept.
