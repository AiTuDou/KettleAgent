import sys
import time

#
# A class that handles commands that the agent itself should be handling and not forwarding to the kettle.
# Commands handled:
#   quit - the agent has finished its jobs and should be shut down
#   sleep - the agent should sleep for a given amount of seconds, after which, control should be ceded back to the LLM
#
#   any other commands should be forwarded to the environment (kettle) for execution
class SpecialAgentCommandExecutor:

    def __init__(self, delegated_executor):
        self.delegatedExecutor = delegated_executor
        self.initialisationTime = time.time()

    output = None

    def execute(self, command: str, parameter=None):
        if command == 'quit':
            print("Quitting agent")
            sys.exit()
        elif command == 'sleep':
            print("Agent sleeping for", int(parameter), "seconds")

            time.sleep(int(parameter))
            output = "current agent run time (s): " + str(time.time() - self.initialisationTime)
        else:
            print("Delegating command to kettle: '", command, "'", sep='')
            output = self.delegatedExecutor.execute(command)

        return output
