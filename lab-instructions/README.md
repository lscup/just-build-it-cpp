# Lab Instruction Authoring

The file chapters.json is the shared source for the StudySite and optional
local Grade Calculator lab instructions.

After changing the manifest or an instruction template, regenerate both sets:

    python3 scripts/generate_lab_instructions.py

Then validate that all generated files are current and that the two
environment workflows remain separate:

    python3 scripts/generate_lab_instructions.py --check
    python3 scripts/validate_lab_instructions.py

Generated output:

- studysite-labs/ — StudySite internal editor, Run, embedded Terminal, Tutor,
  and Load from GitHub/Save to GitHub workflow.
- local-labs/ — local editor, C++17 compiler, executable, Git commit, and push
  workflow.

Do not hand-edit generated chapter files. Update chapters.json or the generator
so both instruction sets stay aligned.
