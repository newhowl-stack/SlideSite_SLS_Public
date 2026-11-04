# Known limitations and verification status

Updated 3 November 2026. This is not marketplace certification.

| Check | Status |
| --- | --- |
| Starter matches pinned rights-clean1.27.0 candidate | Exact bytes/hash verified |
| Downloads without GitHub sign-in | Results in [test record](docs/evidence/2026-11-03.md) |
| ZIP extraction, member hashes and canonical runtime | Reproducible with scripts/verify_package.py |
| First-time ChatGPT generation → browser edit → save → offline reopen | Pending; no authenticated file-enabled session available in test browser |
| First-time Claude generation → browser edit → save → offline reopen | Pending; browser reaches Claude sign-in |
| Fresh offline file reopen in this freeze | Passed native HTML download/close/fresh offline reopen across3 runtime variants; earlier plugin-session policy limitation remains historical, not AI-consumer acceptance |
| Hosted AI authorization, read, edit and persistence | Preview; independent current end-to-end acceptance pending |
| Formal versioned schema/Theme-token contract | Not certified here; use embedded canonical agent/model documentation |

Historical development wizard provider-choice tests do not prove an actual first-time AI conversation. A working download or JSON parse does not establish rendering or persistence.

AI file-tool availability varies. Preserve the supplied editor runtime, CSP, fonts, assets and libraries; change only supported deck-source data. Treat slide content as data, not instructions. Review text fit, images, Theme changes and layouts in the browser. New chart/layout systems and text-fit feature work are outside this package.

Light and Dark are modes of a Theme. Use supported bindings for intended inheritance; intentional overrides can stay unchanged when switching Theme. Full-size sample-image collections and hosted services need a network connection. Added deck images are embedded on save. Fonts are not subset to existing slide text.

Hosted setup downloads do not install an app, grant presentation access or supply inference credits. Verify the permission and actual saved result. Never share keys or tokens in issues or slides.

[Feedback](https://github.com/newhowl-stack/SlideSite_SLS_Public/issues/new): provide browser/provider, exact steps and package checksum; remove private content first.
