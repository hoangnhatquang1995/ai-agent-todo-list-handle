import agent

if __name__ == "__main__":
    user_input = ""
    while user_input.lower() not in ["q", "quit", "exit"]:
        user_input = input("You: ")
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Exiting the program. Goodbye!")
            break
        response = agent.talk_to_agent(user_input)
        print(f"Agent: {response['messages'][-1].content}")