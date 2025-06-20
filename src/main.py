"""Entry point for running the culture fit interview simulator."""

from agents import (
    CompanyCultureRetrieverAgent,
    CandidateProfileAgent,
    QuestionGeneratorAgent,
    ResponseEvaluatorAgent,
    ResponseCoachingAgent,
    CulturalCues,
    CandidateProfile,
)


def run_example():
    """Run an example workflow using placeholder data."""
    retriever = CompanyCultureRetrieverAgent()
    profile_agent = CandidateProfileAgent()
    question_agent = QuestionGeneratorAgent()
    evaluator = ResponseEvaluatorAgent()
    coach = ResponseCoachingAgent()

    # Placeholder inputs
    cues = retriever.retrieve(["company_values.pdf"])
    profile = profile_agent.build_profile("resume.pdf", "https://linkedin.com/in/example", "I value collaboration and innovation.")

    questions = question_agent.generate(cues, profile)
    responses = ["sample response"]
    evaluation = evaluator.evaluate(responses, cues)
    feedback = coach.coach(responses, evaluation, cues)

    print("Questions:", questions)
    print("Evaluation:", evaluation)
    print("Coaching feedback:", feedback)


if __name__ == "__main__":
    run_example()
