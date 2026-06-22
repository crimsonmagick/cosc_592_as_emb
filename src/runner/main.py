from src.runner.compiler import GnuCompilerCollection, OptimizationLevel


def main():
    print("hey")
    gcc = GnuCompilerCollection()
    object_file = gcc.compile('../native/functions/factorial.c',
                '../../out', OptimizationLevel.OFF)
    print(object_file)


if __name__ == "__main__":
    main()
