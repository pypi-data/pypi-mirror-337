import logging
import re
import shutil
from pathlib import Path

import click

from ..core.config import ConfigManager
from ..core.packaging import ArtifactBuilder, is_valid_artifact_name_version, normalize_artifact_name
from ..utils.error_handler import MurError
from ..utils.loading import Spinner
from .base import ArtifactCommand

logger = logging.getLogger(__name__)


class BuildCommand(ArtifactCommand):
    """Handles artifact building.

    This class manages the process of building Murmur artifacts (agents or tools)
    by creating the necessary directory structure and configuration files.

    Attributes:
        verbose (bool): Whether to enable verbose output.
        current_dir (Path): The current working directory.
        yaml (YAML): Configured YAML parser instance.
        build_manifest (dict): The loaded build manifest configuration.
        artifact_type (str): Type of artifact ('agent' or 'tool').
        config (dict): The build configuration (alias for build_manifest).
    """

    def __init__(self, verbose: bool = False, scope: str | None = None) -> None:
        """Initialize build command.

        Args:
            verbose: Whether to enable verbose output
            scope: Scope for the artifact (alphanumeric only, will be converted to lowercase)

        Raises:
            MurError: If initialization fails
        """
        try:
            super().__init__('build', verbose)
            self.verbose = verbose
            self.scope = scope  # update scope in parent

            # Load and validate manifest
            self.build_manifest = self._load_build_manifest()
            self.artifact_type = self._validate_artifact_type(self.build_manifest.get('type', ''))

            if not self.is_private_registry:
                if self.scope is None:
                    self._get_scope_from_user()

        except Exception as e:
            if not isinstance(e, MurError):
                raise MurError(code=207, message=str(e), original_error=e)
            raise

    def _get_scope_from_user(self) -> None:
        """Set scope from user accounts.

        Loads user accounts from config and prompts user to select one if multiple exist.

        Raises:
            MurError: If no user accounts are found or if loading fails
        """
        try:
            config_manager = ConfigManager()
            config = config_manager.get_config()
            user_accounts = config.get('user_accounts', [])

            if user_accounts and len(user_accounts) > 1:
                self.scope = click.prompt('Select account', type=click.Choice(user_accounts), show_choices=True)
            else:
                if not user_accounts:
                    raise MurError(
                        code=310,
                        message='No scope specified',
                        detail="Please use 'mur build --scope <scope>' to specify a scope for building a public artifact",
                    )
        except Exception as e:
            if not isinstance(e, MurError):
                raise MurError(
                    code=507,
                    message='Failed to get user accounts',
                    detail='Could not retrieve user accounts from configuration',
                    original_error=e,
                )
            raise

    def _validate_artifact_type(self, artifact_type: str) -> str:
        """Validate the artifact type.

        Args:
            artifact_type: The artifact type to validate

        Returns:
            The validated artifact type

        Raises:
            MurError: If the artifact type is invalid
        """
        if artifact_type not in ['agent', 'tool']:
            raise MurError(
                code=207,
                message=f"Invalid artifact type '{artifact_type}'",
                detail="The artifact type in murmur-build.yaml must be either 'agent' or 'tool'.",
                debug_messages=[f'Found artifact_type: {artifact_type}'],
            )
        return artifact_type

    def _load_build_manifest(self) -> dict:
        """Load manifest from murmur-build.yaml.

        Returns:
            dict: Manifest configuration dictionary.

        Raises:
            MurError: If manifest file is missing or invalid YAML.
        """
        manifest_file = self.current_dir / 'murmur-build.yaml'
        if not manifest_file.exists():
            raise MurError(
                code=201,
                message='murmur-build.yaml not found',
                detail='The murmur-build.yaml manifest file was not found in the current directory',
            )

        try:
            with open(manifest_file) as f:
                return self.yaml.load(f)
        except Exception as e:
            raise MurError(code=205, message='Failed to load murmur-build.yaml', original_error=e)

    def _create_directory_structure(self, artifact_path: Path) -> None:
        """Create the artifact directory structure.

        Creates the necessary artifact directories and files for the artifact,
        including the murmur namespace artifact structure and source files.
        If source files exist in the current directory, they will be copied over.
        If no source files exist, a default main.py will be created.

        Args:
            artifact_path (Path): Root path for new artifact.

        Raises:
            MurError: If directory creation fails, required files are missing,
                or source file copying fails.
        """
        try:
            # Create murmur namespace artifact structure
            src_path = artifact_path / 'src' / 'murmur' / 'artifacts'
            src_path.mkdir(parents=True, exist_ok=True)

            artifact_name = artifact_path.name
            artifact_path = Path(f'{self.scope}_{artifact_name}' if self.scope else artifact_name)
            namespace_path = src_path / artifact_path
            namespace_path.mkdir(parents=True, exist_ok=True)

            # Create an empty __init__.py
            with open(namespace_path / '__init__.py', 'w') as f:
                pass

            logger.debug(f'Created directory structure at {artifact_path}')

            # Handle source files
            if (self.current_dir / 'src').exists():
                src_files = list((self.current_dir / 'src').glob('*.py'))
                if src_files and not (self.current_dir / 'src' / 'main.py').exists():
                    raise MurError(
                        code=201,
                        message='main.py is missing',
                        detail='Source files found but main.py is missing. main.py is required as the default entry point.',
                    )
                elif (main_file := self.current_dir / 'src' / 'main.py').exists():
                    shutil.copy(main_file, namespace_path)
                    if self.verbose:
                        logger.info('Copying source files...')
                    logger.debug(f'Copied main.py to {namespace_path}')
            else:
                # Create default main.py if no source files exist
                with open(namespace_path / 'main.py', 'w') as f:
                    f.write('from murmur.build import ActivateAgent\n\n')
                    f.write(f"{artifact_name} = ActivateAgent('{artifact_name}')\n")
                logger.debug(f'Created default main.py with {artifact_name} function')

        except Exception as e:
            raise MurError(code=209, message='Failed to create directory structure', original_error=e)

    def _create_project_files(self, artifact_path: Path) -> None:
        """Create all necessary project files.

        Creates README.md and pyproject.toml files for the artifact with appropriate
        content based on the build configuration.

        Args:
            artifact_path (Path): Root path for new artifact.

        Raises:
            MurError: If file creation fails.
        """
        try:
            # Create README.md
            with open(artifact_path / 'README.md', 'w') as f:
                f.write(f"# {self.build_manifest['name']}\n\n{self.build_manifest.get('description', '')}")

            # Create pyproject.toml
            with open(artifact_path / 'pyproject.toml', 'w') as f:
                f.write(self._generate_pyproject_toml())

            logger.debug('Created project files')
            if self.verbose:
                logger.info('Created project configuration files')

        except Exception as e:
            raise MurError(code=210, message='Failed to create project files', original_error=e)

    def _generate_pyproject_toml(self) -> str:
        """Generate pyproject.toml content.

        Combines all project configuration sections into a complete pyproject.toml file.

        Returns:
            str: Complete content for pyproject.toml file.
        """
        content = []
        content.extend(self._generate_build_system())
        content.extend(self._generate_project_section())
        content.extend(self._generate_project_urls())
        content.extend(self._generate_build_targets())
        return '\n'.join(content)

    def _generate_build_system(self) -> list[str]:
        """Generate build-system section.

        Returns:
            list[str]: Lines for the build-system section of pyproject.toml.
        """
        return [
            '[build-system]',
            'requires = ["hatchling<=1.26.3"]  # pypiserver 2.3.2 requires hatchling metadata version up to version 2.3',
            'build-backend = "hatchling.build"',
            '',
        ]

    def _generate_project_section(self) -> list[str]:
        """Generate project section including metadata.

        Returns:
            list[str]: Lines for the project section of pyproject.toml, including
                name, version, description, and other metadata.
        """
        if not self.is_private_registry and not self.scope:
            raise MurError(
                code=507,
                message='No scope set',
                detail="A scope is required for publishing to the public registry. Please run 'mur login' first.",
            )
        prefix = f'{self.scope}-' if not self.is_private_registry else ''
        artifact_name = f'{prefix}{self.build_manifest["name"]}'.lower()
        content = [
            '[project]',
            f'name = "{artifact_name}"',
            f'version = "{self.build_manifest["version"]}"',
        ]

        metadata = self.build_manifest.get('metadata', {})

        # Add optional fields
        if description := self.build_manifest.get('description'):
            content.append(f'description = "{description}"')

        if requires_python := metadata.get('requires_python'):
            content.append(f'requires-python = "{requires_python}"')

        # Add author information
        content.extend(self._generate_authors(metadata))

        # Add license
        if license_type := metadata.get('license'):
            content.append(f'license = {{text = "{license_type}"}}')

        # Add classifiers
        content.extend(self._generate_classifiers(license_type))
        content.append('readme = "README.md"')

        # Add dependencies
        content.extend(self._generate_dependencies())

        return content

    def _generate_authors(self, metadata: dict) -> list[str]:
        """Generate authors section if author info exists.

        Creates the authors section of pyproject.toml based on provided metadata.

        Args:
            metadata (dict): Dictionary containing author metadata including 'author'
                and optional 'email' fields.

        Returns:
            list[str]: Lines for the authors section of pyproject.toml.
        """
        if author := metadata.get('author'):
            email = metadata.get('email', '')
            author_line = '{name = "' + author + '"'
            if email:
                author_line += f', email = "{email}"'
            author_line += '}'
            return ['authors = [', f'    {author_line}', ']']
        return []

    def _generate_classifiers(self, license_type: str | None) -> list[str]:
        """Generate classifiers section.

        Args:
            license_type: Type of license for the project, if any.

        Returns:
            list[str]: Lines for the classifiers section of pyproject.toml.
        """
        classifiers = [
            'classifiers = [',
            '    "Programming Language :: Python",',
            '    "Programming Language :: Python :: 3",',
            '    "Programming Language :: Python :: 3 :: Only",',
            '    "Intended Audience :: Developers",',
            '    "Intended Audience :: Information Technology",',
            '    "Intended Audience :: System Administrators",',
        ]

        if license_type:
            classifiers.append(f'    "License :: OSI Approved :: {license_type} License",')

        classifiers.extend(
            [
                '    "Topic :: Software Development :: Libraries :: Python Modules",',
                '    "Topic :: Scientific/Engineering :: Artificial Intelligence",',
                ']',
            ]
        )
        return classifiers

    def _generate_dependencies(self) -> list[str]:
        """Generate dependencies section.

        Returns:
            list[str]: Lines for the dependencies section of pyproject.toml.
        """
        if dependencies := self.build_manifest.get('dependencies', []):
            return ['requires_dist = [', *[f'    "{dep}",' for dep in dependencies], ']']
        return ['requires_dist = []']

    def _generate_project_urls(self) -> list[str]:
        """Generate project.urls section.

        Returns:
            list[str]: Lines for the project.urls section of pyproject.toml.
        """
        valid_url_types = {'repository', 'documentation', 'project'}
        urls = self.build_manifest.get('metadata', {}).get('urls', {})
        valid_urls = {
            url_type: url_list[0] for url_type, url_list in urls.items() if url_type in valid_url_types and url_list
        }

        if not valid_urls:
            return []

        content = ['', '[project.urls]']
        for url_type, url in valid_urls.items():
            title = url_type.capitalize()
            content.append(f'{title} = "{url}"')
        return content

    def _generate_build_targets(self) -> list[str]:
        """Generate build targets section.

        Returns:
            list[str]: Lines for the build targets section of pyproject.toml.
        """
        return ['', '[tool.hatch.build.targets.wheel]', 'packages = ["src/murmur"]']

    def _write_filtered_build_manifest(self, artifact_name: Path) -> None:
        """Filter and write configuration to murmur-build.yaml.

        Writes a filtered version of the configuration to the artifact's
        murmur-build.yaml file, including only the relevant keys for the
        artifact type. For agents, this includes the 'instructions' key.

        Args:
            artifact_name (Path): Path to new artifact.

        Raises:
            MurError: If writing config fails.
        """
        # Base allowed keys for all artifact types
        allowed_keys = {'name', 'version', 'type', 'description', 'dependencies', 'metadata'}

        # Add instructions key only for agent type
        if self.artifact_type == 'agent':
            allowed_keys.add('instructions')

        filtered_config = {k: v for k, v in self.build_manifest.items() if k in allowed_keys}

        name = f'{self.scope}_{artifact_name.name}' if self.scope is not None else artifact_name.name

        artifact_entry_path = artifact_name / 'src' / 'murmur' / 'artifacts' / name

        try:
            with open(artifact_entry_path / 'murmur-build.yaml', 'w') as f:
                f.write('# This file is automatically generated based on murmur-build.yaml in the parent directory\n')
                self.yaml.dump(filtered_config, f)

            logger.debug(f'Written config keys to murmur-build.yaml: {list(filtered_config.keys())}')
        except Exception as e:
            raise MurError(code=205, message='Failed to write murmur-build.yaml', original_error=e)

    def _build_artifact(self, artifact_path: Path) -> None:
        """Build the artifact for publishing.

        Args:
            artifact_path: Path to the artifact directory containing pyproject.toml

        Raises:
            MurError: If the artifact build process fails.
        """
        try:
            builder = ArtifactBuilder(artifact_path, self.verbose)
            result = builder.build(self.artifact_type)
            logger.debug(f"Built artifact files: {', '.join(result.distribution_files)}")
        except MurError as e:
            e.handle()
            raise

    def execute(self) -> None:
        """Execute the build command.

        Creates a new artifact project with the specified configuration,
        including directory structure, project files, and filtered config.
        If the artifact directory already exists, the build will be skipped.

        Raises:
            MurError: If build process fails at any stage.
        """
        try:
            # Validate the artifact name and version
            is_valid_artifact_name_version(self.build_manifest['name'], self.build_manifest['version'])

            # Determine artifact path
            artifact_name = normalize_artifact_name(self.build_manifest['name'])
            artifact_path = self.current_dir / artifact_name

            if artifact_path.exists():
                logger.info(
                    f"The {self.artifact_type} '{artifact_name}' has already been built in this directory. "
                    f'To rebuild, please remove the existing {artifact_name} directory first.'
                )
                return

            spinner = Spinner()
            try:
                if not (self.verbose or logger.getEffectiveLevel() <= logging.DEBUG):
                    spinner.start(f'Building {self.artifact_type} {artifact_name}')

                # Build artifact
                self._create_directory_structure(artifact_path)
                self._create_project_files(artifact_path)
                self._write_filtered_build_manifest(artifact_path)
                self._build_artifact(artifact_path)

            finally:
                if not (self.verbose or logger.getEffectiveLevel() <= logging.DEBUG):
                    spinner.stop()

            self.log_success(
                f"Successfully built {self.artifact_type} "
                f"{self.build_manifest['name']} {self.build_manifest['version']}"
            )

        except MurError as e:
            e.handle()


def build_command() -> click.Command:
    """Create the build command for Click.

    Returns:
        Click command for building artifacts
    """

    @click.command()
    @click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
    @click.option(
        '--scope', type=str, help='Scope for the artifact (alphanumeric only, will be converted to lowercase)'
    )
    def build(verbose: bool, scope: str | None = None) -> None:
        """Build a new artifact project."""
        try:
            # Validate scope format if provided
            if scope:
                # Use regex to ensure only alphanumeric characters
                if not re.match(r'^[a-zA-Z0-9]+$', scope):
                    raise MurError(
                        code=507,
                        message='Invalid scope format',
                        detail='Scope must contain only alphanumeric characters (no spaces, hyphens, or special characters).',
                    )

                # Convert to lowercase if provided
                scope_value = scope.lower()
            else:
                scope_value = None

            # Pass the scope to the BuildCommand constructor
            cmd = BuildCommand(verbose=verbose, scope=scope_value)
            cmd.execute()
        except MurError as e:
            e.handle()

    return build
