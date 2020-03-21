import sys


class Application:

    def __init__(self):
        self.load_config()

    def load_config(self):
        try:
            # ...
        except Exception as e:
            print("\nError %s" % str(e), file=sys.stderr)
            sys.stderr.flush()
            sys.exit(1)

    def run(self):
        pass


def run():
    Application("%s(prog)s [OPTIONS]").run()


if __name__ == '__main__':
    run()
