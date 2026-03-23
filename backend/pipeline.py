from __future__ import annotations

from typing import Any, Dict, List

# CrewAI imports removed to avoid OpenAI dependency
# from crewai import Agent as CrewAgent
# from crewai import Crew, Process, Task as CrewTask

from backend.agents.analysis_agent import AnalysisAgent
from backend.agents.research_agent import ResearchAgent
from backend.agents.summary_agent import SummaryAgent
from models.llm_model import get_llm


class ResearchPipeline:
    """
    Multi-agent pipeline:
    User Query -> ResearchAgent -> AnalysisAgent -> SummaryAgent -> Output

    Notes on CrewAI usage:
    - We instantiate a CrewAI crew (agents + tasks) to reflect the multi-agent architecture.
    - Execution here is deterministic via our Python agent classes (more reliable offline).
    - The CrewAI objects are available for future extension to fully LLM-driven task execution.
    """

    def __init__(self):
        self.llm = get_llm()
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent(llm=self.llm)
        self.summary_agent = SummaryAgent(llm=self.llm)
        # CrewAI crew creation removed to avoid OpenAI dependency
        # self._crew: Optional[Crew] = self._build_crew()

    # CrewAI crew building removed to avoid OpenAI API key requirement
    # def _build_crew(self) -> Crew:
    #     # These CrewAI agents model the system roles; the pipeline is executed by code.
    #     research = CrewAgent(
    #         role="Research Agent",
    #         goal="Search the web and collect relevant energy research sources",
    #         backstory="You are a meticulous web researcher focused on energy topics.",
    #         llm=self.llm,
    #         verbose=False,
    #     )
    #     analysis = CrewAgent(
    #         role="Analysis Agent",
    #         goal="Extract key insights and remove irrelevant information",
    #         backstory="You are an analytical energy domain expert.",
    #         llm=self.llm,
    #         verbose=False,
    #     )
    #     summary = CrewAgent(
    #         role="Summary Agent",
    #         goal="Write a structured research report with clear sections",
    #         backstory="You are a technical writer for energy research.",
    #         llm=self.llm,
    #         verbose=False,
    #     )

    #     tasks = [
    #         CrewTask(description="Research the query and gather sources.", expected_output="A set of sources and corpus.", agent=research),
    #         CrewTask(description="Analyze corpus and extract key points.", expected_output="Bullet-point key findings.", agent=analysis),
    #         CrewTask(description="Generate a structured report.", expected_output="Title/Intro/Findings/Conclusion.", agent=summary),
    #     ]
    #     return Crew(agents=[research, analysis, summary], tasks=tasks, process=Process.sequential, verbose=False)

    # @property
    # def crew(self) -> Crew:
    #     assert self._crew is not None
    #     return self._crew

    def run(self, query: str) -> Dict[str, Any]:
        research_out = self.research_agent.run(query)
        analysis_out = self.analysis_agent.run(query=research_out.query, raw_corpus=research_out.raw_corpus)
        report = self.summary_agent.run(query=query, key_points=analysis_out.key_points)

        return {
            "query": query,
            "sources": research_out.sources,
            "analysis_key_points": analysis_out.key_points,
            "report": {
                "title": report.title,
                "introduction": report.introduction,
                "key_findings": report.key_findings,
                "conclusion": report.conclusion,
            },
        }

