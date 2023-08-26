import sys


class Migration:

    def up(self):
        print(f'[UP] {self.__class__.__name__}')

    def down(self):
        print(f'[DOWN] {self.__class__.__name__}')

    def run(self):
        if len(sys.argv) == 1:
            sys.exit(
                'Error: You need to choice between "up" or "down" method to run.'
            )

        arg = sys.argv[1]
        if arg.lower() == 'up':
            self.up()

        elif arg.lower() == 'down':
            self.down()

        else:
            sys.exit(
                'Error: You need to choice only between "up" or "down" method to run.'
            )
