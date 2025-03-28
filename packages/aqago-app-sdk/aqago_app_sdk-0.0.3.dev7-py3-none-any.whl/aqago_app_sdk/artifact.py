import subprocess
import sys


class Artifact:
    def __init__(
        self, name, version, metadata, url, digest, tags, variant, get, reference=None
    ):
        self.name = name
        self.version = version
        self.metadata = metadata
        self.url = url
        self.digest = digest
        self.tags = tags
        self.variant = variant
        self.get = get
        self.reference = reference

    def fetch(self):
        if not self.reference:
            raise ValueError("Artifact reference is required to fetch the artifact.")
        try:
            result = subprocess.check_output(
                ["aqago-agent", "fetch-artifact", self.reference],
                stderr=subprocess.STDOUT,
                text=True,
            )
            return result
        except FileNotFoundError as e:
            print(
                f"Error: Command 'aqago-agent fetch-artifact {self.reference}' not found. Is the agent running?",
                file=sys.stderr,
            )
            raise RuntimeError(f"Agent not running: {e}") from e
        except subprocess.CalledProcessError as e:
            print(
                f"Error: Command 'aqago-agent fetch-artifact {self.reference}' failed with return code {e.returncode}",
                file=sys.stderr,
            )
            print(f"Output: {e.output}", file=sys.stderr)
            raise RuntimeError(f"Command failed: {e}") from e
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            raise RuntimeError(f"Unexpected error: {e}") from e
