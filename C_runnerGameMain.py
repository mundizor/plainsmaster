import C_gameMain

class RunnerGameMain(C_gameMain.GameMain):
    def __init__(self, plainmasterTeam, keys, networkHandler, window):
        C_gameMain.GameMain.__init__(self, plainmasterTeam, keys, networkHandler, window)

    def on_mouse_press(self, x,y,button,modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy, window):
        pass