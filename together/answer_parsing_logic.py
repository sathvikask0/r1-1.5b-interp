import re

def extract_answer(pred_str, use_last_number=True):
    """
    Extracts the answer from a prediction string.
    This minimal version looks for the token "boxed" and extracts what follows.
    """
    # Remove any unwanted Unicode substring.
    pred_str = pred_str.replace("\u043a\u0438", "")
    pred = ""
    
    if "boxed" in pred_str:
        ans = pred_str.split("boxed")[-1]
        if not ans:
            return ""
        # If the answer is enclosed in curly braces, extract the content.
        if ans[0] == "{":
            stack = 1
            a = ""
            for c in ans[1:]:
                if c == "{":
                    stack += 1
                    a += c
                elif c == "}":
                    stack -= 1
                    if stack == 0:
                        break
                    a += c
                else:
                    a += c
            pred = a
        else:
            # Otherwise, take up to the first "$" (if present) or the whole trimmed string.
            pred = ans.split("$")[0].strip()
    
    # Remove any newlines and trim unwanted starting/ending characters.
    pred = re.sub(r"\n\s*", "", pred)
    if pred.startswith(":"):
        pred = pred[1:]
    if pred.endswith("."):
        pred = pred[:-1]
    if pred.endswith("/"):
        pred = pred[:-1]
    return pred

def strip_string(string):
    """
    Minimal version of string cleaning: just remove leading and trailing whitespace.
    """
    return str(string).strip()

def math_equal(pred, gt, timeout=True):
    """
    Minimal math equality: checks if the cleaned strings are exactly equal.
    """
    return strip_string(pred) == strip_string(gt)

def check_is_correct(pred, gt, timeout=True):
    """
    Returns True if the prediction equals the ground truth (after minimal cleaning).
    """
    return math_equal(strip_string(pred), strip_string(gt), timeout=timeout)


# Minimal demonstration of the functionality.
if __name__ == "__main__":
    # Dummy list of generated responses and corresponding ground-truth answers.
    generated_responses = [
        "Some text boxed{42}",
        "Answer is boxed{3.14}",
        "Info: boxed{100}."
    ]
    # Dummy value for args.data_name (unused in this minimal version)
    data_name = "dummy"
    ground_truths = ["42", "3.14", "100"]

    generated_answers = [extract_answer(response, data_name) for response in generated_responses]
    is_correct_list = [check_is_correct(gen_ans, gt) for gen_ans, gt in zip(generated_answers, ground_truths)]

    print("Generated Answers:", generated_answers)
    print("Correctness:", is_correct_list)
