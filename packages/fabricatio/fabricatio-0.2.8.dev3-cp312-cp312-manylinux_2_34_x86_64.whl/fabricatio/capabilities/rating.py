"""A module that provides functionality to rate tasks based on a rating manual and score range."""

from itertools import permutations
from random import sample
from typing import Dict, List, Optional, Set, Tuple, Union, Unpack, overload

from fabricatio._rust_instances import TEMPLATE_MANAGER
from fabricatio.config import configs
from fabricatio.journal import logger
from fabricatio.models.kwargs_types import ValidateKwargs
from fabricatio.models.usages import LLMUsage
from fabricatio.parser import JsonCapture
from fabricatio.utils import override_kwargs
from more_itertools import flatten, windowed
from pydantic import NonNegativeInt, PositiveInt


class Rating(LLMUsage):
    """A class that provides functionality to rate tasks based on a rating manual and score range.

    References:
        Lu X, Li J, Takeuchi K, et al. AHP-powered LLM reasoning for multi-criteria evaluation of open-ended responses[A/OL]. arXiv, 2024. DOI: 10.48550/arXiv.2410.01246.
    """

    async def rate_fine_grind(
        self,
        to_rate: str | List[str],
        rating_manual: Dict[str, str],
        score_range: Tuple[float, float],
        **kwargs: Unpack[ValidateKwargs[Dict[str, float]]],
    ) -> Optional[Dict[str, float] | List[Dict[str, float]]]:
        """Rate a given string based on a rating manual and score range.

        Args:
            to_rate (str): The string to be rated.
            rating_manual (Dict[str, str]): A dictionary containing the rating criteria.
            score_range (Tuple[float, float]): A tuple representing the valid score range.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            Dict[str, float]: A dictionary with the ratings for each dimension.
        """

        def _validator(response: str) -> Dict[str, float] | None:
            if (
                (json_data := JsonCapture.validate_with(response, dict, str))
                and json_data.keys() == rating_manual.keys()
                and all(score_range[0] <= v <= score_range[1] for v in json_data.values())
            ):
                return json_data
            return None

        logger.info(f"Rating for {to_rate}")
        return await self.aask_validate(
            question=(
                TEMPLATE_MANAGER.render_template(
                    configs.templates.rate_fine_grind_template,
                    {
                        "to_rate": to_rate,
                        "min_score": score_range[0],
                        "max_score": score_range[1],
                        "rating_manual": rating_manual,
                    },
                )
            )
            if isinstance(to_rate, str)
            else [
                TEMPLATE_MANAGER.render_template(
                    configs.templates.rate_fine_grind_template,
                    {
                        "to_rate": item,
                        "min_score": score_range[0],
                        "max_score": score_range[1],
                        "rating_manual": rating_manual,
                    },
                )
                for item in to_rate
            ],
            validator=_validator,
            **kwargs,
        )

    @overload
    async def rate(
        self,
        to_rate: str,
        topic: str,
        criteria: Set[str],
        score_range: Tuple[float, float] = (0.0, 1.0),
        **kwargs: Unpack[ValidateKwargs],
    ) -> Dict[str, float]: ...

    @overload
    async def rate(
        self,
        to_rate: List[str],
        topic: str,
        criteria: Set[str],
        score_range: Tuple[float, float] = (0.0, 1.0),
        **kwargs: Unpack[ValidateKwargs],
    ) -> List[Dict[str, float]]: ...

    async def rate(
        self,
        to_rate: Union[str, List[str]],
        topic: str,
        criteria: Set[str],
        score_range: Tuple[float, float] = (0.0, 1.0),
        **kwargs: Unpack[ValidateKwargs],
    ) -> Optional[Dict[str, float] | List[Dict[str, float]]]:
        """Rate a given string or a sequence of strings based on a topic, criteria, and score range.

        Args:
            to_rate (Union[str, List[str]]): The string or sequence of strings to be rated.
            topic (str): The topic related to the task.
            criteria (Set[str]): A set of criteria for rating.
            score_range (Tuple[float, float], optional): A tuple representing the valid score range. Defaults to (0.0, 1.0).
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            Union[Dict[str, float], List[Dict[str, float]]]: A dictionary with the ratings for each criterion if a single string is provided,
            or a list of dictionaries with the ratings for each criterion if a sequence of strings is provided.
        """
        manual = await self.draft_rating_manual(topic, criteria, **kwargs) or dict(zip(criteria, criteria, strict=True))

        return await self.rate_fine_grind(to_rate, manual, score_range, **kwargs)

    async def draft_rating_manual(
        self, topic: str, criteria: Optional[Set[str]] = None, **kwargs: Unpack[ValidateKwargs[Dict[str, str]]]
    ) -> Optional[Dict[str, str]]:
        """Drafts a rating manual based on a topic and dimensions.

        Args:
            topic (str): The topic for the rating manual.
            criteria (Optional[Set[str]], optional): A set of criteria for the rating manual. If not specified, then this method will draft the criteria automatically.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            Dict[str, str]: A dictionary representing the drafted rating manual.
        """

        def _validator(response: str) -> Dict[str, str] | None:
            if (
                (json_data := JsonCapture.validate_with(response, target_type=dict, elements_type=str)) is not None
                and json_data.keys() == criteria
                and all(isinstance(v, str) for v in json_data.values())
            ):
                return json_data
            return None

        criteria = criteria or await self.draft_rating_criteria(topic, **override_kwargs(dict(kwargs), default=None))

        if criteria is None:
            logger.error(f"Failed to draft rating criteria for topic {topic}")
            return None

        return await self.aask_validate(
            question=(
                TEMPLATE_MANAGER.render_template(
                    configs.templates.draft_rating_manual_template,
                    {
                        "topic": topic,
                        "criteria": criteria,
                    },
                )
            ),
            validator=_validator,
            **kwargs,
        )

    async def draft_rating_criteria(
        self,
        topic: str,
        criteria_count: NonNegativeInt = 0,
        **kwargs: Unpack[ValidateKwargs[Set[str]]],
    ) -> Optional[Set[str]]:
        """Drafts rating dimensions based on a topic.

        Args:
            topic (str): The topic for the rating dimensions.
            criteria_count (NonNegativeInt, optional): The number of dimensions to draft, 0 means no limit. Defaults to 0.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            Set[str]: A set of rating dimensions.
        """
        return await self.aask_validate(
            question=(
                TEMPLATE_MANAGER.render_template(
                    configs.templates.draft_rating_criteria_template,
                    {
                        "topic": topic,
                        "criteria_count": criteria_count,
                    },
                )
            ),
            validator=lambda resp: set(out)
            if (out := JsonCapture.validate_with(resp, list, str, criteria_count)) is not None
            else out,
            **kwargs,
        )

    async def draft_rating_criteria_from_examples(
        self,
        topic: str,
        examples: List[str],
        m: NonNegativeInt = 0,
        reasons_count: PositiveInt = 2,
        criteria_count: PositiveInt = 5,
        **kwargs: Unpack[ValidateKwargs],
    ) -> Optional[Set[str]]:
        """Asynchronously drafts a set of rating criteria based on provided examples.

        This function generates rating criteria by analyzing examples and extracting reasons for comparison,
        then further condensing these reasons into a specified number of criteria.

        Parameters:
            topic (str): The subject topic for the rating criteria.
            examples (List[str]): A list of example texts to analyze.
            m (NonNegativeInt, optional): The number of examples to sample from the provided list. Defaults to 0 (no sampling).
            reasons_count (PositiveInt, optional): The number of reasons to extract from each pair of examples. Defaults to 2.
            criteria_count (PositiveInt, optional): The final number of rating criteria to draft. Defaults to 5.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for validation.

        Returns:
            Set[str]: A set of drafted rating criteria.

        Warnings:
            Since this function uses pairwise comparisons, it may not be suitable for large lists of examples.
            For that reason, consider using a smaller list of examples or setting `m` to a non-zero value smaller than the length of the examples.
        """
        if m:
            examples = sample(examples, m)

        # extract reasons from the comparison of ordered pairs of extracted from examples
        reasons = flatten(
            await self.aask_validate(
                question=[
                    TEMPLATE_MANAGER.render_template(
                        configs.templates.extract_reasons_from_examples_template,
                        {
                            "topic": topic,
                            "first": pair[0],
                            "second": pair[1],
                            "reasons_count": reasons_count,
                        },
                    )
                    for pair in (permutations(examples, 2))
                ],
                validator=lambda resp: JsonCapture.validate_with(
                    resp, target_type=list, elements_type=str, length=reasons_count
                ),
                **kwargs,
            )
        )
        # extract certain mount of criteria from reasons according to their importance and frequency
        return await self.aask_validate(
            question=(
                TEMPLATE_MANAGER.render_template(
                    configs.templates.extract_criteria_from_reasons_template,
                    {
                        "topic": topic,
                        "reasons": list(reasons),
                        "criteria_count": criteria_count,
                    },
                )
            ),
            validator=lambda resp: set(out)
            if (out := JsonCapture.validate_with(resp, target_type=list, elements_type=str, length=criteria_count))
            else None,
            **kwargs,
        )

    async def drafting_rating_weights_klee(
        self,
        topic: str,
        criteria: Set[str],
        **kwargs: Unpack[ValidateKwargs[float]],
    ) -> Dict[str, float]:
        """Drafts rating weights for a given topic and criteria using the Klee method.

        Args:
            topic (str): The topic for the rating weights.
            criteria (Set[str]): A set of criteria for the rating weights.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            Dict[str, float]: A dictionary representing the drafted rating weights for each criterion.
        """
        if len(criteria) < 2:  # noqa: PLR2004
            raise ValueError("At least two criteria are required to draft rating weights")

        criteria_seq = list(criteria)  # freeze the order
        windows = windowed(criteria_seq, 2)

        # get the importance multiplier indicating how important is second criterion compared to the first one
        relative_weights = await self.aask_validate(
            question=[
                TEMPLATE_MANAGER.render_template(
                    configs.templates.draft_rating_weights_klee_template,
                    {
                        "topic": topic,
                        "first": pair[0],
                        "second": pair[1],
                    },
                )
                for pair in windows
            ],
            validator=lambda resp: JsonCapture.validate_with(resp, target_type=float),
            **kwargs,
        )
        weights = [1]
        for rw in relative_weights:
            weights.append(weights[-1] * rw)
        total = sum(weights)
        return dict(zip(criteria_seq, [w / total for w in weights], strict=True))

    async def composite_score(
        self,
        topic: str,
        to_rate: List[str],
        reasons_count: PositiveInt = 2,
        criteria_count: PositiveInt = 5,
        **kwargs: Unpack[ValidateKwargs],
    ) -> List[float]:
        """Calculates the composite scores for a list of items based on a given topic and criteria.

        Args:
            topic (str): The topic for the rating.
            to_rate (List[str]): A list of strings to be rated.
            reasons_count (PositiveInt, optional): The number of reasons to extract from each pair of examples. Defaults to 2.
            criteria_count (PositiveInt, optional): The number of criteria to draft. Defaults to 5.
            **kwargs (Unpack[ValidateKwargs]): Additional keyword arguments for the LLM usage.

        Returns:
            List[float]: A list of composite scores for the items.
        """
        criteria = await self.draft_rating_criteria_from_examples(
            topic, to_rate, reasons_count, criteria_count, **kwargs
        )
        weights = await self.drafting_rating_weights_klee(topic, criteria, **kwargs)
        logger.info(f"Criteria: {criteria}\nWeights: {weights}")
        ratings_seq = await self.rate(to_rate, topic, criteria, **kwargs)

        return [sum(ratings[c] * weights[c] for c in criteria) for ratings in ratings_seq]
