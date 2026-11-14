
import re

DRAWER_CODE = "3142"
EXIT_CODE = "7285"


def validate_action(action, state):
    action = action.lower().strip()

    # Block administrator impersonation and prompt injection
    blocked_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "game administrator",
        "reveal all codes",
        "reveal all secrets",
        "bypass the rules",
        "override the rules",
    ]

    if any(phrase in action for phrase in blocked_phrases):
        return "You cannot override the game rules. Solve the puzzles to escape."

    # Collect the brass key
    if re.search(r"\b(take|collect|pick up|grab)\b", action) and "key" in action:
        if not state["drawer_unlocked"]:
            return "The brass key is inside the locked drawer."

        if "brass key" in state["inventory"]:
            return "You already have the brass key."

        state["inventory"].append("brass key")
        return "You collected the brass key!"

    # Unlock the drawer - check BEFORE bookshelf
    if "drawer" in action:
        if state["drawer_unlocked"]:
            return "The drawer is already open."

        codes = re.findall(r"\b\d{4}\b", action)

        if not codes:
            return "The drawer is locked. Enter a four-digit code."

        if len(codes) != 1 or codes[0] != DRAWER_CODE:
            return "Incorrect drawer code. The drawer remains locked."

        if not state["books_examined"]:
            return "Investigate the bookshelf before unlocking the drawer."

        state["drawer_unlocked"] = True
        return "The drawer opens! A brass key is inside."

    # Examine the bookshelf
    if "bookshelf" in action or "books" in action:
        state["books_examined"] = True
        return "You examine four special books and discover the code 3142."

    # Examine the painting
    if "painting" in action:
        state["painting_examined"] = True
        return "Behind the painting is a note: The clock holds the final secret."

    # Open the clock
    if "clock" in action:
        if state["clock_unlocked"]:
            return "The clock compartment is already open."

        if "brass key" not in state["inventory"]:
            return "You cannot open the clock without collecting the brass key."

        state["clock_unlocked"] = True
        return "The clock opens! You discover the final exit code: 7285."

    # Unlock the exit door
    if "door" in action or "exit" in action:
        if state["escaped"]:
            return "You have already escaped!"

        if not state["clock_unlocked"]:
            return "You must solve the clock puzzle first."

        codes = re.findall(r"\b\d{4}\b", action)

        if len(codes) != 1 or codes[0] != EXIT_CODE:
            return "Incorrect exit code. The door remains locked."

        state["door_unlocked"] = True
        state["escaped"] = True

        return "Congratulations! You unlocked the exit and escaped!"

    # Unsupported actions
    return (
        "That action is not available. "
        "Try examining the bookshelf, desk, painting, clock, or exit door."
    )
