import logging
from typing import Iterator, List

import huggingface_hub
from pydantic import BaseModel, Field

from morphius.core.exceptions.base import MethodNotImplementedError
from morphius.core.models.evaluator import (
    AnyKeywordBasedPromptEvaluation,
    EvaluationModelName,
    EvaluationModelType,
    ModelBasedPromptEvaluation,
)
from morphius.core.models.prompts import Turn


class MultiTurnConversation(BaseModel):
    turns: List[Turn]
    unsafe: bool
    jailbreak: bool = False
    language: str = "en"
    redacted: bool = False
    complexity: int = 3
    base_prompt: str = ""  # Real red team prompt without any morphing
    goal: str  # Real goal of the prompt
    harmful_tags: List[str] = Field(default_factory=list)
    evaluation_hint: ModelBasedPromptEvaluation | AnyKeywordBasedPromptEvaluation = (
        ModelBasedPromptEvaluation(
            eval_model_type=EvaluationModelType.TOXICITY,
            eval_model_name=EvaluationModelName.ANY,
        )
    )


class BaseRiskPromptGenerator:
    HF_DATASET_NAME = ""

    REGISTERED_DATASET_NAME = ""

    DESCRIPTION = ""

    RISK_MAP = {}

    POLICY_TO_GOAL_MAP = {}

    def generate(self, risk_name: str) -> Iterator[MultiTurnConversation]:
        raise MethodNotImplementedError()

    def support_risk_class(self, risk_class: str) -> bool:
        return risk_class in self.RISK_MAP.keys()

    def get_supported_risk_classes(self) -> List[str]:
        return list(self.RISK_MAP.keys())

    def get_description(self) -> str:
        return self.DESCRIPTION

    @classmethod
    def is_available(cls) -> bool:
        """Check if the dataset is available on Hugging Face Hub."""
        try:
            api = huggingface_hub.HfApi()
            dataset_info = api.dataset_info(cls.HF_DATASET_NAME)
            return dataset_info is not None  # If dataset info exists, return True
        except huggingface_hub.errors.HfHubHTTPError:
            return False  # Dataset not available or network issue

    def get_labels(self, risk_class: str) -> List[str]:
        """
        Retrieves labels related to the risk_class
        """
        category_labels = self.RISK_MAP.get(risk_class, [])
        return category_labels

    def get_goals(self, risk_class: str) -> List[str]:
        """
        Retrieves a list of goal descriptions for a given risk class by mapping
        policies from RISK_MAP to POLICY_TO_GOAL_MAP.

        :param risk_class: The risk class name.
        :return: A list of goal descriptions corresponding to the mapped policies.
        """
        category_labels = self.RISK_MAP.get(risk_class, [])
        if not category_labels:
            logging.warning(f"Risk class '{risk_class}' not found in RISK_MAP.")
            return []

        goals = [
            self.POLICY_TO_GOAL_MAP[policy]
            for policy in category_labels
            if policy in self.POLICY_TO_GOAL_MAP
        ]

        return goals

    def get_all_goals(self) -> List[str]:
        return self.POLICY_TO_GOAL_MAP.values()
