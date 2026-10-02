# Dev Container

`devcontainer.json` lets VS Code or Cursor (with the Dev Containers extension)
open this repository inside a container built from the repository's
`Dockerfile`:

1. Start Docker.
2. Open the repository and choose **Reopen in Container**.
3. In the container's terminal, run `./reproduce.sh`.

The repository is mounted at `/remark`, so edits and regenerated outputs land
in your working copy. The Python environment, installed from `uv.lock`, lives
at `/opt/venv` inside the container rather than in the shared `.venv`.
