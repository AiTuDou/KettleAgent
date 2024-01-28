import time

from GptApiInputCommandSource import GptApiInputCommandSource
from KeyboardInputCommandSource import KeyboardInputCommandSource
from SpecialAgentCommandExecutor import SpecialAgentCommandExecutor
from WebSocketCommandExecutor import WebSocketCommandExecutor

commandExecutor = None
commandSource = None

if __name__ == '__main__':
    print("Running")

    # commandSource = KeyboardInputCommandSource()
    commandSource = GptApiInputCommandSource()
    webSocketCommandExecutor = WebSocketCommandExecutor()
    commandExecutor = SpecialAgentCommandExecutor(webSocketCommandExecutor)

    prompt = "Boil the kettle"

    while True:
        generatedCommand = commandSource.generate_command(prompt)
        prompt = commandExecutor.execute(generatedCommand[0], generatedCommand[1])