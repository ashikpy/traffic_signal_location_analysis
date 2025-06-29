def fancy_text_box(message: str) -> str:
    padding = 2
    width = len(message) + padding * 2
    top = "╔" + "═" * width + "╗"
    middle = f"║{' ' * padding}{message}{' ' * padding}║"
    bottom = "╚" + "═" * width + "╝"
    print(f"{top}\n{middle}\n{bottom}")
