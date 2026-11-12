from functions.write_file import write_file


def main():
    cases = [
        ("lorem.txt", "wait, this isn't lorem ipsum"),
        ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("/tmp/temp.txt", "this should not be allowed"),
    ]
    for file_path, content in cases:
        print(f"Result for '{file_path}':")
        print(write_file("calculator", file_path, content))
        print()


if __name__ == "__main__":
    main()
