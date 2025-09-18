# Documentation Instructions

Goal: Create one markdown file per section that documents the private helper methods used by the `DataQualityLibrary` class for that section. The files live next to the sample metadata and are named:

- `row_processing.md` — documents row-processing helper methods
- `field_validation.md` — documents field-level validation helper methods
- `custom_validation.md` — documents custom validation helper methods

Each section file should contain, for every private method referenced by that section:

- **Short description:** one-line purpose
- **How it works:** implementation summary and behaviour (rows affected, columns added, side-effects)
- **Example input parameters:** a short JSON snippet taken from the sample metadata that exercises that helper
- **Example result:** brief, concrete description of changes to the DataFrame (columns added, rows dropped/flagged)

Suggested workflow to keep docs current:

1. When adding a new action/type to a metadata file, add or update the corresponding method doc in the section file.
2. Include the metadata snippet under "Example input parameters" so future readers can map metadata → method call.
3. If the implementation changes, update the "How it works" and "Example result" sections and add a date/short changelog line.

Where to put new docs:
- Keep docs alongside sample metadata in `sample_metadata/` for discoverability. If you prefer an API-style folder, move them into `docs/api/` and update any README references.

Next steps you can run (optional):

```
# open the files or commit them
code .\sample_metadata\row_processing.md; code .\sample_metadata\field_validation.md; code .\sample_metadata\custom_validation.md
```
