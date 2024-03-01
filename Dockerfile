FROM ghcr.io/sacdallago/biotrainer:latest

ENTRYPOINT ["/app/.venv/bin/python", "-m", "autoeval.utilities.cli"]