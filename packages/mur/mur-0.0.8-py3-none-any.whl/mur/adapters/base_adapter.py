import logging
from abc import ABC, abstractmethod
from typing import Any

from ..core.packaging import ArtifactManifest

logger = logging.getLogger(__name__)


class RegistryAdapter(ABC):
    """Base adapter for registry interactions.

    This abstract class defines the interface for registry adapters that handle
    artifact publishing and artifact index management.

    Args:
        verbose (bool, optional): Enable verbose logging output. Defaults to False.
    """

    def __init__(self, verbose: bool = False, index_url: str | None = None):
        self.verbose = verbose
        self.index_url = index_url
        if verbose:
            logger.setLevel(logging.DEBUG)

    @abstractmethod
    def publish_artifact(
        self,
        manifest: ArtifactManifest,
        scope: str | None = None,
    ) -> dict[str, Any]:
        """Publish an artifact to the registry.

        Args:
            manifest (ArtifactManifest): The artifact manifest containing metadata and file info
            scope (str | None, optional): The scope of the artifact. Defaults to None.

        Returns:
            dict[str, Any]: Response data from the registry after publishing

        Raises:
            NotImplementedError: This is an abstract method that must be implemented
        """
        pass

    @abstractmethod
    def get_artifact_indexes(self) -> list[str]:
        """Get list of artifact index URLs for installation.

        Returns:
            list[str]: List of PyPI-compatible index URLs in priority order

        Raises:
            NotImplementedError: This is an abstract method that must be implemented
        """
        pass
