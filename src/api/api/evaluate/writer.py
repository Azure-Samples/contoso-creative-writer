from promptflow.evals.evaluators import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator

class WriterEvaluator:
    def __init__(self, model_config):
        self.evaluators = [
            RelevanceEvaluator(model_config),
            FluencyEvaluator(model_config),
            CoherenceEvaluator(model_config),
            GroundednessEvaluator(model_config),
        ]

    def __call__(self, *, query: str, context: str, response: str, **kwargs):
        output = {}
        for evaluator in self.evaluators:
            result = evaluator(
                question=query,
                context=context,
                answer=response,
            )
            output.update(result)
        return output
