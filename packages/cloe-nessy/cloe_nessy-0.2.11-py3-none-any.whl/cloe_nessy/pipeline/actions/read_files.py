from typing import Any

from ...integration.reader import FileReader
from ..pipeline_action import PipelineAction
from ..pipeline_context import PipelineContext


class ReadFilesAction(PipelineAction):
    """Reads files from a specified location.

    If an extension is provided, all files with the given extension will be read
    using the [`FileReader`][cloe_nessy.integration.reader.file_reader]. If no
    extension is provided, the `spark_format` must be set, and all files in the
    location will be read using a DataFrameReader with the specified format.

    Example:
    ```yaml
    Read Excel Table:
        action: READ_FILES
        options:
            location: excel_file_folder/excel_files_june/
            search_subdirs: True
            spark_format: AVRO
    ```
    """

    name: str = "READ_FILES"

    @staticmethod
    def run(
        context: PipelineContext,
        *,
        location: str | None = None,
        search_subdirs: bool = False,
        extension: str | None = None,
        spark_format: str | None = None,
        schema: str | None = None,
        add_metadata_column: bool = True,
        options: dict[str, str] | None = None,
        **_: Any,
    ) -> PipelineContext:
        """Reads files from a specified location.

        Args:
            context: The context in which this Action is executed.
            location: The location from which to read files.
            search_subdirs: Recursively search subdirectories for files
                if an extension is provided.
            extension: The file extension to filter files by.
            spark_format: The format to use for reading the files.
            schema: The schema of the data. If None, schema is obtained from
                the context metadata.
            add_metadata_column: Whether to include the `__metadata` column with
                file metadata in the DataFrame.
            options: Additional options passed to the reader.

        Raises:
            ValueError: If neither `extension` nor `spark_format` are provided, or if
                no location is specified.

        Returns:
            The context after the Action has been executed, containing the read data as a DataFrame.
        """
        if not location:
            raise ValueError("No location provided. Please specify location to read files from.")
        if not options:
            options = dict()

        if (metadata := context.table_metadata) and schema is None:
            schema = metadata.schema

        file_reader = FileReader()
        if extension:
            df = file_reader.read(
                location=location,
                schema=schema,
                extension=extension,
                search_subdirs=search_subdirs,
                options=options,
                add_metadata_column=add_metadata_column,
            )
        elif spark_format:
            df = file_reader.read(
                location=location,
                schema=schema,
                spark_format=spark_format,
                options=options,
                add_metadata_column=add_metadata_column,
            )
        else:
            raise ValueError("Please provide either the 'extension' or 'spark_format'")

        runtime_info = context.runtime_info

        if add_metadata_column:
            read_files_list = [x.file_path for x in df.select("__metadata.file_path").drop_duplicates().collect()]
            if runtime_info is None:
                runtime_info = {"read_files": read_files_list}
            else:
                try:
                    runtime_info["read_files"] = list(set(runtime_info["read_files"] + read_files_list))
                except KeyError:
                    runtime_info["read_files"] = read_files_list

        return context.from_existing(data=df, runtime_info=runtime_info)
