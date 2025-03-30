"""Example of using the library."""

import asyncio
from pathlib import Path

from fabricatio import Event, Role, WorkFlow, logger
from fabricatio.actions.article import (
    FixIllegalReferences,
    FixIntrospectedErrors,
    GenerateArticle,
    GenerateArticleProposal,
    GenerateInitialOutline,
    TweakOutlineBackwardRef,
    TweakOutlineForwardRef,
)
from fabricatio.actions.article_rag import TweakArticleRAG
from fabricatio.actions.output import DumpFinalizedOutput, PersistentAll
from fabricatio.models.task import Task


async def main() -> None:
    """Main function."""
    Role(
        name="Undergraduate Researcher",
        description="Write an outline for an article in typst format.",
        llm_top_p=0.8,
        llm_temperature=1.15,
        llm_model="openai/deepseek-v3-250324",
        llm_rpm=1000,
        llm_tpm=1000000,
        llm_max_tokens=8190,
        registry={
            Event.quick_instantiate(ns := "article"): WorkFlow(
                name="Generate Article Outline",
                description="Generate an outline for an article. dump the outline to the given path. in typst format.",
                steps=(
                    GenerateArticleProposal(llm_temperature=1.18),
                    GenerateInitialOutline(output_key="article_outline",llm_temperature=1.21, llm_top_p=0.5),
                    FixIntrospectedErrors(output_key="article_outline"),
                    FixIllegalReferences(output_key="article_outline"),
                    TweakOutlineBackwardRef(output_key="article_outline"),
                    TweakOutlineForwardRef(output_key="article_outline"),
                    FixIllegalReferences(output_key="article_outline"),
                    GenerateArticle(output_key="article", llm_temperature=1.2, llm_top_p=0.45),
                    PersistentAll,
                    TweakArticleRAG(output_key="to_dump", llm_temperature=1.2, llm_top_p=0.45),
                    DumpFinalizedOutput(output_key="task_output"),
                    PersistentAll,
                ),
            ).update_init_context(
                article_briefing=Path("./article_briefing.txt").read_text(),
                dump_path="out.typ",
                persist_dir="persistent",
                collection_name="article_essence"
            )
        },
    )

    proposed_task = Task(name="write an article")
    path = await proposed_task.delegate(ns)
    logger.success(f"The outline is saved in:\n{path}")


if __name__ == "__main__":
    asyncio.run(main())
