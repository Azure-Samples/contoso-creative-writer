# Microsoft AI Evaluator API and Custom Evaluators with Prompty

**Evaluation is critical** to ensure that AI systems behave as intended and meet the desired standards for safety, quality, and alignment with business goals. Azure AI leverages  to allows developers to systematically test generative ai with  prebuilt and custom evaluators.  This flexible framework ensures that AI outputs meet robust quality standards and align with specific business needs.

**Pre-built evaluators** Azure AI SDK provides a library of built-in evaluators for safety and quality metrics. These can be leveraged using the evaluator library in the Azure SDK. The prebuilt evaluators were designed with a broad set of guidelines.

**Custom Evaluators** let you define your own evaluation metrics in the event that a prebuilt evaluator metric needs to be refined or customized, or a pre-built evaluator does not exist do not cover a particular behavior you would like to measure i.e. *friendliness*. 

### More reading:  ###
[AI-Assisted Evaluations](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai#ai-assisted-evaluations)

[Evaluation and monitoring metrics for generative AI](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-metrics-built-in?tabs=warning)

## Exercise: Working with Evaluators

In this open-ended exercise, you test using AI-Assisted Evaluation on your application prototype by working with prebuilt evaluators, creating your own custom evaluator, and using built-in tracing to demo observability. Reference existing code in this repository to add to the solution. 

### Task 1: Add a Prebuilt Evaluator

1. Navigate to the `src/api/evaluate` directory and review the pre-built evaluators being used in `evaluate.py`, 
2. Comparing `evaluate.py` to the list of prebuilt evaluators available in the [API documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk), select one prebuilt evaluator that's not already included and add it to `evaluate.py`
3. Test your work and ensure the orchestrator passes content to evaluator and retrieves the evaluation results. Note: you may need to update the parameter `evaluate=false` to enable the evaluator. 

### Task 2: Review a sample custom evaluator

1. Navigate to the `src/api/evaluators/friendliness` directory.
2. Open the `friendliness.prompty` file and review its structure. This is an example of a custom evaluator. 
3. Open the `friendliness_evaluator.py` file and review the `evaluate()` function implementation.
4. Test the friendliness evaluator and observe its results.

### Task 3: Create your own custom evaluator

1. Come up with your own custom evaluator that you would like to add to Contoso creative writer.
2. Create a new .prompty file in `src/api/evaluate` and name it after the type of behavior you would like to test, similar to the existing `friendliness.prompty`. 
3. Design a system prompt and examples to evaluate your of AI-generated content. Use the `friendliness.prompty` file as a guide. 
4. Create a `.py` file for your new evaluator in the same directory similar to `friendliness.py`.
5. Test your new custom evaluator and observe its results.

### Bonus Challenge: Putting it all together.

1. Open the `orchestrator.py` file in the `src/api` directory. Ensure that your application is set you automatically evaluate images and articles, and ensure your new evaluators are running.
2. Activate the prompty tracing server and analyze the tracing for your application. 