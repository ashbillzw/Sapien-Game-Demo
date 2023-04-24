import numpy as np

import sapien

import maploader


class Game(object):
    def __init__(self):
        self.gametick = 0

        engine = sapien.core.Engine()
        renderer = sapien.core.SapienRenderer()

        engine.set_renderer(renderer)

        self.scene = engine.create_scene()
        self.scene.set_timestep(1 / 300.0)

        self.viewer = sapien.utils.Viewer(renderer)
        self.viewer.set_scene(self.scene)

        self.init_scene()
        self.init_camera()

        while not self.viewer.closed:
            self.update()

    def init_scene(self):
        self.scene.add_ground(altitude=-100)

        self.scene.set_ambient_light([0.5, 0.5, 0.5])
        self.scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    def init_camera(self):
        self.viewer.set_camera_xyz(-4, 0, 2)
        self.viewer.set_camera_rpy(0,-45, 0)
        self.viewer.window.set_camera_parameters(0.05, 100, 1)

    def update(self):
        self.scene.step()

        if self.gametick % 5 == 0:
            self.scene.update_render()
            self.viewer.render()

        self.gametick += 1



def main():
    game = Game()

if __name__ == '__main__':
    main()
