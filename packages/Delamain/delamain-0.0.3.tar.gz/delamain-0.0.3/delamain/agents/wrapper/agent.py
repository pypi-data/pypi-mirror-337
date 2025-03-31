from collections.abc import AsyncIterator
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic_ai.messages import (
    AgentStreamEvent,
    ModelMessage,
)
from pydantic_ai.models import KnownModelName, Model
from pydantic_ai.settings import ModelSettings
from pydantic_ai.tools import ToolDefinition
from pydantic_ai.usage import Usage

from delamain.agents.base import DelamainAgent
from delamain.agents.executor import Executor
from delamain.agents.utils import get_model
from delamain.config import get_config

_HERE = Path(__file__).parent
env = Environment(loader=FileSystemLoader(_HERE / "prompts"), autoescape=True)

DEFAULT_EXECUTOR_SYSTEM_PROMPT_TEMPLATE = "executor_system_prompt.md"


def render_template(template_file_name: str, **kwargs):
    template = env.get_template(template_file_name)
    return template.render(**kwargs)


class DelamainWrapper(DelamainAgent):
    @classmethod
    def from_config(
        cls,
        messages: list[ModelMessage],
        executor_tools: list[ToolDefinition] | None = None,
    ):
        config = get_config()
        return cls(
            messages=messages,
            executor_tools=executor_tools,
            executor_model=config.executor_model,
            executor_system_prompt=config.executor_system_prompt,
            executor_model_settings=config.executor_model_settings,
            custom_instructions=config.custom_instructions,
        )

    def __init__(
        self,
        messages: list[ModelMessage],
        executor_tools: list[ToolDefinition] | None = None,
        executor_model: Model | KnownModelName | None = None,
        *,
        executor_system_prompt: str | None = None,
        executor_model_settings: ModelSettings | None = None,
        custom_instructions: str | None = None,
    ):
        self.messages = messages
        self.usage = Usage()
        self.executor_tools = executor_tools or []

        self.executor = Executor(
            get_model(executor_model),
            system_prompt=executor_system_prompt
            or render_template(
                DEFAULT_EXECUTOR_SYSTEM_PROMPT_TEMPLATE,
                custom_instructions=custom_instructions,
            ),
            model_settings=executor_model_settings,
            tools=self.executor_tools,
        )

    async def run(self) -> AsyncIterator[AgentStreamEvent]:
        async for event in self.executor.run(None, self.messages):
            yield event
