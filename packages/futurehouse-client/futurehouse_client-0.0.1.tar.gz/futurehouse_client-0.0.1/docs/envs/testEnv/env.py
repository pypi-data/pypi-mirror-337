from aviary.core import Environment, Tool, Message
from pydantic import BaseModel

class ExampleState(BaseModel):
    reward: float
    done: bool
    a: int
    b: int


class ExampleEnv(Environment[ExampleState]):
    state: ExampleState

    @Environment.tool()
    def increment_a(self, state: ExampleState) -> None:
        """Increment the value of 'a' by 1"""
        state.a += 1

    @Environment.tool()
    def increment_b(self, state: ExampleState) -> None:
        """Increment the value of 'b' by 1"""
        state.b += 1
    
    @Environment.tool()
    def set_done(self, state: ExampleState) -> None:
        """Set the done flag to True"""
        state.done = True

    @Environment.tool()
    def check_done(self, state: ExampleState) -> bool:
        """Check if the environment is done"""
        return state.done

    async def reset(self) -> tuple[list[Message], list[Tool]]:
        self.tools = [
            Tool.from_function(self.increment_a),
            Tool.from_function(self.increment_b),
            Tool.from_function(self.set_done),
            Tool.from_function(self.check_done),
        ]
        start = Message("Randomly increment a and b 50 times and check if done. Tell me the final values of a and b when you are done")
        return [start], self.tools

    async def step(self, action: Message) -> tuple[list[Message], ExampleState]:
        msgs = await self.execute_tools(action, state = self.state)
        return msgs, self.state, self.state.done, False
