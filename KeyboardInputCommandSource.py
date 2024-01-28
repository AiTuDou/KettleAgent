class KeyboardInputCommandSource:
    def generate_command(self, prompt: str):
        print("Current prompt: " + prompt)
        keyboard_inputs = input().split()

        if len(keyboard_inputs) > 1:
            return (keyboard_inputs[0], keyboard_inputs[1])
        else:
            return (keyboard_inputs[0], None)