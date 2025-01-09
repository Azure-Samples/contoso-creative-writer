from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory

class MainDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "MainDialog"):
        super(MainDialog, self).__init__(dialog_id or MainDialog.__name__)

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [self.initial_step, self.process_step, self.final_step],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> WaterfallStepContext:
        return await step_context.prompt(
            "TextPrompt",
            PromptOptions(prompt=MessageFactory.text("What is your name?")),
        )

    async def process_step(self, step_context: WaterfallStepContext) -> WaterfallStepContext:
        # Store the user's name in dialog state
        step_context.values["name"] = step_context.result
        return await step_context.prompt(
            "TextPrompt",
            PromptOptions(
                prompt=MessageFactory.text(
                    f"Hello {step_context.result}! How can I assist you today?"
                )
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext) -> WaterfallStepContext:
        user_message = step_context.result

        # Here you could integrate the UniversalReasoning module
        # For example, you might access it via the bot's context
        # Since it's not directly available here, we'll pass the message back

        # Send a confirmation message to the user
        await step_context.context.send_activity(
            MessageFactory.text(f"You said: {user_message}")
        )

        return await step_context.end_dialog()
