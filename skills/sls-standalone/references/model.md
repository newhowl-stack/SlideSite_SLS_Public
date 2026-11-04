# Model reference — SLS 1.0 / editor 2.8.0 / runtime 1.27.1 routing derivative

Authoritative payload: the real `<script id="deck-source" type="application/json">` element. Schema: `presentation-studio/2`. Do not replace it with an outline.

Keep format/version keys, canvas, Theme, legacy metadata, assets, font_faces, fonts, sls_structure and view. Slides have stable id, name, description (intent), purpose, layout, section_id, background, background_binding and objects. Native text example:

```json
{"id":"unique-headline-id","type":"text","role":"headline","html":"Meet less. Decide more.","x":135,"y":110,"w":1600,"h":190,"size":76,"family":"display","weight":700,"line_height":1.16,"color":"#182B49","style_bindings":{"color":"text","family":"display"},"z":0,"reading_order":0}
```

Coordinates use the deck canvas (this starter: 1920 × 1080). Text size and all geometry are slide units. Use generous spacing, bounded text and escaped HTML. Style bindings refer to existing Theme token/font roles. Do not invent new Theme definitions. Referenced image assets must exist in assets; fonts required by font_faces must remain available.

`sls_structure.outline` lists slide names. Sections and `new_presentation_brief` must agree with intended structure, titles and purpose. Do not erase an existing library or deliberate overrides. The helper marks the derived index stale after raw editing; the trusted editor refreshes its normal index on export. Exact JSON is always authoritative.


Use the bundled assets/manifest.json for the exact pinned starter. Preserve the existing seven Theme families, embedded fonts, libraries and Light/Dark modes. No schema upgrade or editor change is part of generation. Final schema sign-off and platform acceptance are separate from structural checks.
