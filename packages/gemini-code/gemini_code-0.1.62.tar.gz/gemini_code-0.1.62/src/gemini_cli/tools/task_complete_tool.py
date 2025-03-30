"""
Tool to signal task completion.
"""
import logging
from .base import BaseTool

log = logging.getLogger(__name__)

class TaskCompleteTool(BaseTool):
    """
    Signals that the current task/request is fully completed.
    This MUST be the final tool called by the assistant for a given request.
    """
    name = "task_complete"
    description = "Signals task completion. MUST be called as the final step, providing a user-friendly summary."

    def execute(self, summary: str) -> str:
        """
        Signals completion and returns the summary provided by the LLM.

        Args:
            summary: A concise, user-friendly summary of the actions taken and the final outcome.

        Returns:
            The summary string provided as input. The orchestrator uses this call as a signal to stop.
        """
        log.info(f"Task completion signaled by LLM.")
        log.debug(f"LLM Summary provided: {summary}")
        if not summary or not isinstance(summary, str) or len(summary) < 5:
             log.warning("TaskCompleteTool called with missing or very short summary.")
             # Provide a default confirmation if summary is bad/missing
             return "Task marked as complete, but the provided summary was insufficient."
        # The orchestrator loop will see this tool was called and use this summary.
        # We just return the summary itself.
        return summary