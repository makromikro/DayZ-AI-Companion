from dayz.state_reader import load_companion_state


state = load_companion_state()

if state is None:
    print("No companion state found.")
else:
    print(state)