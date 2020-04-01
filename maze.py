import os


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg  # return path


def main():
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Generate and display mazes")
    parser.add_argument('-p', '--path', action='store',
                        help="file that contains maze or that maze will be writte to", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
