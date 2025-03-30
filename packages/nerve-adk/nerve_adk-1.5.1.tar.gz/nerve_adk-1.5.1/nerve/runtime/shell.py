from loguru import logger
from termcolor import colored

from nerve.runtime import state
from nerve.runtime.agent import Agent


class Shell:
    def __init__(self) -> None:
        self._keep_going: bool = False
        # TODO: can we build this by inspecting the class methods?
        self.commands = [
            {
                "name": "quit",
                "description": "Stop the execution and exit.",
                "aliases": ["q", "exit"],
                "action": self._handle_quit,
            },
            {
                "name": "continue",
                "description": "Continue the execution until completion.",
                "aliases": ["c", "cont", "go"],
                "action": self._handle_continue,
            },
            {
                "name": "step",
                "description": "Execute a single step.",
                "aliases": ["", "s"],
                "action": self._handle_step,
            },
            {
                "name": "view",
                "description": "Inspect the current state.",
                "aliases": ["v"],
                "action": self._handle_view,
            },
            {
                "name": "help",
                "description": "Show this help message.",
                "aliases": ["h"],
                "action": self._handle_help,
            },
        ]

    async def _handle_quit(self) -> None:
        logger.warning("👋 quitting")
        exit(0)

    async def _handle_continue(self) -> bool:
        logger.info("▶️  running until completion ...")
        self._keep_going = True
        return True

    async def _handle_step(self) -> bool:
        logger.debug("▶️  single step")
        self._keep_going = False
        return True

    async def _handle_view(self) -> bool:
        usage = state.get_usage()
        print(colored("usage", "white", attrs=["bold"]))
        print(f"  prompt tokens: {usage.prompt_tokens}")
        print(f"  completion tokens: {usage.completion_tokens}")
        print(f"  total tokens: {usage.total_tokens}")
        print(f"  cost: {usage.cost} $")
        print()

        agent = state.get_current_actor()
        print(colored("agent", "white", attrs=["bold"]))
        print(f"  name: {agent.runtime.name}")
        print(f"  model: {agent.configuration.generator}")
        print(f"  conversation strategy: {agent.conv_window_strategy}")
        print()

        vars = state.get_variables()
        if vars:
            print(colored("variables", "white", attrs=["bold"]))
            for k, v in vars.items():
                print(f"  {colored(k, 'green')} = {v}")
            print()

        knowledge = state.get_knowledge()
        if knowledge:
            print(colored("knowledge", "white", attrs=["bold"]))
            for k, v in knowledge.items():
                print(f"  {colored(k, 'green')} = {v}")
            print()

        tools = state.get_tools()
        if tools:
            print(colored("tools", "white", attrs=["bold"]))
            for k in tools.keys():
                print(f"  {colored(k, 'magenta')}")
            print()

        extra_tools = state.get_extra_tools()
        if extra_tools:
            print(colored("extra tools", "white", attrs=["bold"]))
            for k in extra_tools.keys():
                print(f"  {colored(k, 'magenta')}")
            print()

        return False

    async def _handle_help(self) -> bool:
        for cmd in self.commands:
            print(f"  {colored(cmd['name'], 'yellow')} ({', '.join(cmd['aliases'])}): {cmd['description']}")  # type: ignore

        print("\nAnything else will be interpreted and used as a chat message for the current agent.")

        return False

    async def _handle_command(self, command: str) -> tuple[bool, bool]:
        command = command.lower()
        for cmd in self.commands:
            if command in cmd["aliases"] or command == cmd["name"]:  # type: ignore
                done = await cmd["action"]()  # type: ignore
                return True, done

        return False, False

    async def _show_prompt(self, actor: Agent) -> str:
        print()
        prompt = f"{colored(actor.runtime.name, 'yellow')} > "
        command = input(prompt).strip()
        print()

        return command

    async def interact_if_needed(self, actor: Agent) -> None:
        if not state.is_interactive() or self._keep_going:
            return

        # wait for all events to be logged
        state.wait_for_events_logs()

        # show the prompt and get the command
        command = await self._show_prompt(actor)

        # handle the command
        is_handled, done = await self._handle_command(command)
        if not is_handled:
            # anything else is chat
            logger.debug(f"unhandled command: {command}")
            # add the command to the conversation
            actor.add_extra_message(command)
        elif not done:
            # keep running the interaction shell
            await self.interact_if_needed(actor)
