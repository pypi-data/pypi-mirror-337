import json
import subprocess
import sys
from .artifact import Artifact


class GetArtifactException(Exception):
    pass


class AgentNotRunning(Exception):
    pass


class App:
    def __init__(self, reference, deployment, resources):
        self.reference = reference
        self.deployment = deployment
        self.resources = resources

    def get_artifact(self, reference):
        try:
            artifact_data = json.loads(
                subprocess.check_output(
                    ["aqago-agent", "get-artifact", reference]
                ).decode()
            )
            return Artifact(
                name=artifact_data["name"],
                version=artifact_data.get("version"),
                metadata=artifact_data.get("metadata", {}),
                url=artifact_data["url"],
                digest=artifact_data["digest"],
                tags=artifact_data.get("tags", []),
                variant=artifact_data.get("variant"),
                get=artifact_data["get"],
                reference=reference,
            )
        except FileNotFoundError as e:
            print(
                f"Error: Command 'aqago-agent get-artifact {reference}' not found. Is the agent running?",
                file=sys.stderr,
            )
            raise AgentNotRunning(f"Agent not running: {e}") from e
        except subprocess.CalledProcessError as e:
            print(
                f"Error: Command 'aqago-agent get-artifact {reference}' failed with return code {e.returncode}",
                file=sys.stderr,
            )
            print(e.output.decode(), file=sys.stderr)
            raise GetArtifactException(f"Command failed: {e}") from e
        except json.JSONDecodeError as e:
            print(
                f"Error: Failed to decode JSON response for artifact {reference}: {e}",
                file=sys.stderr,
            )
            raise GetArtifactException(f"JSON decode error: {e}") from e
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            raise GetArtifactException(f"Unexpected error: {e}") from e

    @property
    def artifacts(self):
        return ArtifactCollection(self)


# Helper class for dictionary-like artifact access
class ArtifactCollection:
    def __init__(self, app):
        self.app = app

    def __getitem__(self, reference):
        return self.app.get_artifact(reference)


def app(name):
    import json
    import subprocess
    import sys

    try:
        app_data = json.loads(
            subprocess.check_output(["aqago-agent", "get-application", name]).decode()
        )
        return App(
            reference=app_data["reference"],
            deployment=app_data["deployment"],
            resources=app_data.get("resources", []),
        )
    except FileNotFoundError as e:
        print(
            f"Error: Command 'aqago-agent get-application {name}' not found. Is the agent running?",
            file=sys.stderr,
        )
        raise AgentNotRunning(f"Agent not running: {e}") from e
    except subprocess.CalledProcessError as e:
        print(
            f"Error: Command 'aqago-agent get-application {name}' failed with return code {e.returncode}",
            file=sys.stderr,
        )
        print(e.output.decode(), file=sys.stderr)
        raise GetArtifactException(f"Command failed: {e}") from e
    except json.JSONDecodeError as e:
        print(
            f"Error: Failed to decode JSON response for application {name}: {e}",
            file=sys.stderr,
        )
        raise GetArtifactException(f"JSON decode error: {e}") from e
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        raise GetArtifactException(f"Unexpected error: {e}") from e
