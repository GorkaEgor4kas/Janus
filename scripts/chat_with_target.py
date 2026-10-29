from janus.targets.minimal_target import MinimalTarget
from janus.targets.workspace import Workspace

def main() -> None:
    target = MinimalTarget(workspace=Workspace())

    print("Janus Target. Press exit to leave.")

    while True:
        prompt = input("\nYou: ").strip()

        if prompt.lower() in {"exit", "quit"}:
            break

        if not prompt:
            continue

        try:
            response = target.handle(prompt, max_steps=2)
            print(f"\nTarget: {response}")
        except Exception as e:
            print(f"Request Error: {e}")

if __name__ == "__main__":
    main()




