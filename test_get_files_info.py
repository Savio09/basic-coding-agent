from functions.get_files_info import get_files_info


def show(directory: str) -> None:
    label = "current" if directory == "." else f"'{directory}'"
    result = get_files_info("calculator", directory)
    indent = "    " if result.startswith("Error:") else "  "
    print(f"Result for {label} directory:")
    print("\n".join(indent + line for line in result.splitlines()))
    print()


def main():
    show(".")
    show("pkg")
    show("/bin")
    show("../")


if __name__ == "__main__":
    main()
