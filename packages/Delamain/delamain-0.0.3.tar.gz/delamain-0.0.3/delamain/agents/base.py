from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from pydantic_ai.messages import (
    AgentStreamEvent,
    ModelMessage,
)
from pydantic_ai.tools import ToolDefinition


class DelamainAgent(ABC):
    @classmethod
    @abstractmethod
    def from_config(
        cls,
        messages: list[ModelMessage],
        executor_tools: list[ToolDefinition] | None = None,
    ) -> DelamainAgent:
        """Create a DelamainAgent from a configuration object."""

    @abstractmethod
    async def run(self) -> AsyncIterator[AgentStreamEvent]:
        """Run the agent and return a stream of events."""
