# Knowledge governance

- One shared folder per role, not one full copy per person.
- Each person combines company, role-approved, current-project, and private-personal scopes.
- Personal findings enter role candidates first; only evaluated and approved items enter the default role scope.
- Keep GitHub source files readable as folders. ZIP is a distribution artifact, not the live retrieval source.
- Run `scripts/build_knowledge_index.py` to track `source_id` and `content_hash`; unchanged files are skipped, duplicates are reported, and moves can retain identity.
- Retrieve a small matching section plus its heading ancestry and parent summary.
- Run the role evaluation set before activating, replacing, merging, deprecating, or retiring a Skill.
- Do not enable vector retrieval or company-wide permission filtering until scale and measured missed retrieval justify them.
