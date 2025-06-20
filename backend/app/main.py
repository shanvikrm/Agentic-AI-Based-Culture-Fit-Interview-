"""Entry point for running the culture fit interview backend."""

from .agents.culture_retriever import CompanyCultureRetrieverAgent
from .agents.candidate_profile import CandidateProfileAgent
from .agents.question_generator import QuestionGeneratorAgent
from .agents.response_evaluator import ResponseEvaluatorAgent
from .agents.response_coach import ResponseCoachingAgent
from .agents.base import CulturalCues, CandidateProfile


def run_example() -> None:
    """Run an example workflow using placeholder data."""
    retriever = CompanyCultureRetrieverAgent()
    profile_agent = CandidateProfileAgent()
    question_agent = QuestionGeneratorAgent()
    evaluator = ResponseEvaluatorAgent()
    coach = ResponseCoachingAgent()

    cues = retriever.retrieve(["company_values.pdf"])
    profile = profile_agent.build_profile(
        "resume.pdf", "https://linkedin.com/in/example", "I value collaboration"
    )
    questions = question_agent.generate(cues, profile)
    responses = ["sample response"]
    evaluation = evaluator.evaluate(responses, cues)
    feedback = coach.coach(responses, evaluation, cues)

    print("Questions:", questions)
    print("Evaluation:", evaluation)
    print("Coaching feedback:", feedback)


if __name__ == "__main__":
    run_example()
