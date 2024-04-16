import prompty

def design(context, instructions, feedback):
    result = prompty.execute(
        "designer.prompty",
        inputs={"context": context, "instructions": instructions, "feedback": feedback}
    )
    return result

if __name__ == "__main__":
    result = design(
        "The context for the designer.",
        "The instructions for the designer.",
        "The feedback for the designer.")
    print(result)
