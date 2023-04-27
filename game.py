import numpy

import sapien

from table import Table
import map_loader


def get_joints_dict(articulation: sapien.core.Articulation):
    joints = articulation.get_joints()
    joint_names =  [joint.name for joint in joints]
    assert len(joint_names) == len(set(joint_names))
    return {joint.name: joint for joint in joints}


class Game(object):
    def __init__(self):
        self.gametick = 0

        renderer = sapien.core.SapienRenderer()

        engine = sapien.core.Engine()
        engine.set_renderer(renderer)

        self.scene = engine.create_scene()
        self.scene.set_timestep(1 / 300.0)

        self.viewer = sapien.utils.viewer.Viewer(renderer)
        self.viewer.set_scene(self.scene)

        self.init_scene()
        self.init_camera()

        while not self.viewer.closed:
            self.update()
            

    def init_scene(self):
        self.scene.add_ground(altitude=-256)

        self.scene.set_ambient_light([0.5, 0.5, 0.5])
        self.scene.add_directional_light(
            direction = [0, 1, -1],
            color = [0.5, 0.5, 0.5]
        )

        self.table = Table(self.scene)

    def init_camera(self):
        self.viewer.set_camera_xyz(-64, 0, 64)
        self.viewer.set_camera_rpy(0,-45, 0)
        self.viewer.window.set_camera_parameters(0.05, 100, 1)

    def update(self):
        self.scene.step()


        if self.gametick % 5 == 0:
            self.scene.update_render()
            self.viewer.render()

        if self.viewer.window.key_down('i'):
            print("i")
            self.testrollaxlejoint.set_drive_target(0.5)
        elif self.viewer.window.key_down('k'):
            print("k")
            self.testrollaxlejoint.set_drive_target(-0.5)
        else:
            self.testrollaxlejoint.set_drive_target(0.0)
        if self.viewer.window.key_down('j'):
            print("j")
            self.testpitchaxlejoint.set_drive_target(0.5)
        elif self.viewer.window.key_down('l'):
            print("l")
            self.testpitchaxlejoint.set_drive_target(-0.5)
        else:
            self.testpitchaxlejoint.set_drive_target(0.0)
            
        self.gametick += 1


def main():
    game = Game()

if __name__ == '__main__':
    main()
