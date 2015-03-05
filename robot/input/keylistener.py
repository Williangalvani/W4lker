from robot.input import pyxhook


class KeyListener():
    keyMap = {}

    def pressed(self, event ):
        #print key info

        self.keyMap[event.Ascii] = True

    def released(self, event):
        # print dir(event)
                    # print event.Key, event.KeyID
        self.keyMap[event.Ascii] = False

    def get_key(self, key):
        if key in self.keyMap:
            return self.keyMap[key]
        else:
            return False

    def __init__(self):
        self.hookman = pyxhook.HookManager()
        self.hookman.KeyDown = self.pressed
        self.hookman.KeyUp = self.released

        #Hook the keyboard
        self.hookman.HookKeyboard()
        self.hookman.start()

    def __del__(self):
        print "cleaning hook"
        self.hookman.cancel()


if __name__ == "__main__":
    KeyListener()