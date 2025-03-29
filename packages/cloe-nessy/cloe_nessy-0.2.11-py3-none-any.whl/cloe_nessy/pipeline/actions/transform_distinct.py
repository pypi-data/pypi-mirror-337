from typing import Any

from ..pipeline_action import PipelineAction
from ..pipeline_context import PipelineContext


class TransformDistinctAction(PipelineAction):
    """Selects distinct rows from the DataFrame in the given context.

    Example:
    ```yaml
    Decode Columns:
        action: TRANSFORM_DISTINCT
    ```
    """

    name: str = "TRANSFORM_DISTINCT"

    def run(
        self,
        context: PipelineContext,
        **_: Any,
    ) -> PipelineContext:
        """Selects distinct rows from the DataFrame in the given context.

        Args:
            context: The context in which this Action is executed.

        Raises:
            ValueError: If the data from the context is None.

        Returns:
            The context after the execution of this Action, containing the DataFrame with distinct rows.
        """
        if context.data is None:
            raise ValueError("Data from the context is required for the operation.")

        df = context.data.distinct()

        return context.from_existing(data=df)  # type: ignore
