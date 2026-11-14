
import re

CABINET_CODE = "3142"
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
        return (
            "You cannot override the laboratory security rules. "
            "Solve the puzzles to escape."
        )

    # Collect the security access card
    if (
        re.search(r"\b(take|collect|pick up|grab)\b", action)
        and ("card" in action or "access card" in action)
    ):
        if not state["cabinet_unlocked"]:
            return (
                "The security access card is inside "
                "the locked equipment cabinet."
            )

        if "security access card" in state["inventory"]:
            return "You already have the security access card."

        state["inventory"].append("security access card")
        return "You collected the security access card!"

    # Unlock the equipment cabinet
    if "cabinet" in action:
        if state["cabinet_unlocked"]:
            return "The equipment cabinet is already open."

        codes = re.findall(r"\b\d{4}\b", action)

        if not codes:
            return (
                "The equipment cabinet is locked. "
                "Enter a four-digit security code."
            )

        if len(codes) != 1 or codes[0] != CABINET_CODE:
            return (
                "Incorrect security code. "
                "The equipment cabinet remains locked."
            )

        if not state["terminal_examined"]:
            return (
                "Investigate the research terminal "
                "before unlocking the equipment cabinet."
            )

        state["cabinet_unlocked"] = True

        return (
            "The equipment cabinet opens! "
            "A security access card is inside."
        )

    # Examine the research terminal
    if "terminal" in action:
        state["terminal_examined"] = True

        return (
            "You examine the research terminal and discover "
            "four security digits: 3, 1, 4, 2. "
            "The equipment cabinet code is 3142."
        )

    # Examine the security notice board
    if "notice board" in action or "noticeboard" in action:
        state["notice_board_examined"] = True

        return (
            "You discover a hidden security message: "
            "'The reactor control panel holds the final access code.'"
        )

    # Access the reactor control panel
    if "reactor" in action or "control panel" in action:
        if state["reactor_unlocked"]:
            return "The reactor control panel is already unlocked."

        if "security access card" not in state["inventory"]:
            return (
                "Access denied! You must collect "
                "the security access card first."
            )

        state["reactor_unlocked"] = True

        return (
            "Access granted! The reactor control panel unlocks. "
            "You discover the emergency exit code: 7285."
        )

    # Unlock the emergency exit
    if "exit" in action or "door" in action:
        if state["escaped"]:
            return "You have already escaped the laboratory!"

        if not state["reactor_unlocked"]:
            return (
                "The emergency exit is locked. "
                "You must solve the reactor control puzzle first."
            )

        codes = re.findall(r"\b\d{4}\b", action)

        if len(codes) != 1 or codes[0] != EXIT_CODE:
            return (
                "Incorrect emergency exit code. "
                "The security door remains locked."
            )

        state["door_unlocked"] = True
        state["escaped"] = True

        return (
            "Congratulations! You unlocked the emergency exit "
            "and successfully escaped the secret laboratory!"
        )

    # Unsupported actions
    return (
        "That action is not available. Try examining the "
        "research terminal, laboratory workstation, security "
        "notice board, equipment cabinet, reactor control "
        "panel, or emergency exit door."
    )
