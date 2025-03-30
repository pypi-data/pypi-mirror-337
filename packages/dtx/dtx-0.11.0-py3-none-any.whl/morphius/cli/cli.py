import argparse
import logging
import os
import yaml

from dotenv import load_dotenv

from morphius.config import globals
from morphius.core.models.analysis import PromptDataset, RedTeamPlan
from morphius.core.models.providers.base import ProviderType
from morphius.plugins.providers.gradio.cli import GradioProviderGenerator
from morphius.plugins.providers.http.cli import HttpProviderBuilderCli
from morphius.core.repo.plugin import PluginRepo

from .console_output import (
    RichDictPrinter,
    RichResultVisualizer,
    DummyResultCollector,
)
from .providers import ProviderFactory
from .scoping import RedTeamScopeCreator, ScopeInput
from .planner import RedTeamPlanGenerator, PlanInput
from .runner import TestRunInput, RedTeamTestRunner


# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")

logging.basicConfig(level=logging.WARN)


class AgentScanner:
    """Command-line tool to create and manage agent scope YAML files."""

    def __init__(self):
        self.args = self._parse_arguments()

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(description="Agent Scanner CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # --- REDTEAM COMMANDS ---
        redteam_parser = subparsers.add_parser("redteam", help="Red teaming operations")
        redteam_subparsers = redteam_parser.add_subparsers(dest="redteam_command")

        # scope
        scope_parser = redteam_subparsers.add_parser(
            "scope", help="Generate red team scope"
        )
        scope_parser.add_argument("description", type=str, help="Scope description")
        scope_parser.add_argument(
            "output", type=str, nargs="?", default="redteam_scope.yml"
        )

        # plan
        plan_parser = redteam_subparsers.add_parser(
            "plan", help="Generate red team plan"
        )
        plan_parser.add_argument("scope_file", type=str)
        plan_parser.add_argument(
            "output", type=str, nargs="?", default="redteam_plan.yml"
        )
        plan_parser.add_argument("--max_prompts", type=int, default=20)
        plan_parser.add_argument("--prompts_per_risk", type=int, default=5)
        plan_parser.add_argument(
            "--dataset",
            type=PromptDataset,
            required=True,
            choices=PromptDataset.values(),
        )

        # run
        run_parser = redteam_subparsers.add_parser("run", help="Run red team tests")
        run_parser.add_argument("plan_file", type=str)
        run_parser.add_argument(
            "agent", type=ProviderType, choices=ProviderType.values()
        )
        run_parser.add_argument("--url", type=str, default="")
        run_parser.add_argument("--max_prompts", type=int, default=1000000)
        run_parser.add_argument("--tactics", type=str, action="append", default=[])
        run_parser.add_argument("--yml", type=str, default="report.yml")
        run_parser.add_argument(
            "--no-rich", action="store_true", help="Disable rich output"
        )

        # --- PLUGINS COMMANDS ---
        plugins_parser = subparsers.add_parser("plugins", help="Manage plugins")
        plugins_subparsers = plugins_parser.add_subparsers(dest="plugins_command")
        plugins_subparsers.add_parser("list", help="List plugins")

        # --- PROVIDERS COMMANDS ---
        providers_parser = subparsers.add_parser(
            "providers", help="Gradio/HTTP providers"
        )
        providers_subparsers = providers_parser.add_subparsers(dest="providers_command")
        generate_parser = providers_subparsers.add_parser("generate")
        generate_parser.add_argument(
            "provider", type=ProviderType, choices=ProviderType.values()
        )
        generate_parser.add_argument("--url", type=str, default="")
        generate_parser.add_argument("--output", type=str, default="")

        # --- DATASETS / TACTICS ---
        datasets_parser = subparsers.add_parser("datasets")
        datasets_parser.add_subparsers(dest="datasets_command").add_parser("list")

        tactics_parser = subparsers.add_parser("tactics")
        tactics_parser.add_subparsers(dest="tactics_command").add_parser("list")

        return parser.parse_args()

    def run(self):
        match self.args.command:
            case "redteam":
                self._handle_redteam()
            case "providers":
                self._handle_providers()
            case "datasets" if self.args.datasets_command == "list":
                self.list_datasets()
            case "plugins" if self.args.plugins_command == "list":
                self.list_plugins()
            case "tactics" if self.args.tactics_command == "list":
                self.list_tactics()
            case _:
                print("Invalid command. Use --help for usage.")

    def _handle_redteam(self):
        match self.args.redteam_command:
            case "scope":
                self._generate_scope()
            case "plan":
                self._generate_plan()
            case "run":
                self._run_tests()
            case _:
                print("Invalid redteam subcommand")

    def _generate_scope(self):
        config = ScopeInput(description=self.args.description)
        creator = RedTeamScopeCreator(config)
        creator.run()
        creator.save_yaml(self.args.output)

    def _generate_plan(self):
        scope = RedTeamScopeCreator.load_yaml(self.args.scope_file)

        config = PlanInput(
            dataset=self.args.dataset,
            max_prompts=self.args.max_prompts,
            prompts_per_risk=self.args.prompts_per_risk,
        )
        generator = RedTeamPlanGenerator(scope=scope, config=config)
        generator.run()
        generator.save_yaml(self.args.output)

    def _run_tests(self):
        plan = RedTeamPlanGenerator.load_yaml(self.args.plan_file)

        agent = ProviderFactory.get_agent(plan.scope, self.args.agent, self.args.url)
        collector = (
            DummyResultCollector() if self.args.no_rich else RichResultVisualizer()
        )

        config = TestRunInput(
            agent_type=self.args.agent,
            url=self.args.url,
            max_prompts=self.args.max_prompts,
            override_tactics=self.args.tactics,
        )

        runner = RedTeamTestRunner(config)
        runner.run(plan=plan, agent=agent, collector=collector)
        runner.save_yaml(self.args.yml)

    def _handle_providers(self):
        if self.args.providers_command == "generate":
            if self.args.provider == ProviderType.GRADIO:
                generator = GradioProviderGenerator(gradio_url=self.args.url)
                providers = generator.run()
                if providers:
                    generator.save_yaml(providers)
            elif self.args.provider == ProviderType.HTTP:
                builder = HttpProviderBuilderCli(url=self.args.url)
                provider_output = builder.run()
                builder.dump_yaml(provider_output, filename=self.args.output)
            else:
                print("Unsupported provider type for generation.")
        else:
            print("Invalid providers command")

    def list_datasets(self):
        printer = RichDictPrinter("Available Prompt Datasets", "Dataset", "Description")
        printer.print(PromptDataset.descriptions())

    def list_plugins(self):
        plugin_map = PluginRepo.get_plugin_descriptions()
        printer = RichDictPrinter("Available Plugins", "Plugin", "Description")
        printer.print(plugin_map)

    def list_tactics(self):
        tactics_repo = globals.get_tactics_repo(only=True)
        plugin_map = tactics_repo.get_tactics()
        printer = RichDictPrinter("Available Tactics", "Tactic", "Description")
        printer.print(plugin_map)


def main():
    scanner = AgentScanner()
    scanner.run()
