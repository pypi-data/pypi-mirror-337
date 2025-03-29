from .base_strategy import FileRetrievalStrategy
from .local_strategy import LocalDirectoryStrategy


class OneLakeStrategy(FileRetrievalStrategy):
    """Strategy for retrieving files from the OneLake."""

    @staticmethod
    def get_file_paths(location: str, extension: str | None = None, search_subdirs: bool = True) -> list:
        """Recursively retrieves all files with a specified extension from a given directory and its subdirectories.

        Args:
            location: Top-level directory to read from, e.g., '/Volumes/my_volume/landing/example_landing/'.
            extension: File extension, e.g., 'csv', 'json'. Input an empty string to get files without any
                                    extension, input None to get all files.
            search_subdirs: If True, function will also search within all subdirectories.

        Returns:
            List: List of files in the directory and its subdirectories with the given extension.

        Raises:
            ValueError: If the location is not provided.
            Exception: For any other unexpected errors.
        """
        if not location:
            raise ValueError("location is required")

        file_paths = LocalDirectoryStrategy.get_file_paths(location, extension, search_subdirs)

        shortened_file_paths = [p.replace("/lakehouse/default/", "") for p in file_paths]
        return shortened_file_paths
