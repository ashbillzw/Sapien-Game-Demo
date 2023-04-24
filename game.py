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

    # NOTE: How to build actors (rigid bodies) is elaborated in create_actors.py
    # game.scene.add_ground(altitude=0)  # Add a ground
    # actor_builder = game.scene.create_actor_builder()
    # actor_builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
    # actor_builder.add_box_visual(half_size=[0.5, 0.5, 0.5], color=[1., 0., 0.])
    # box = actor_builder.build(name='box')  # Add a box
    # box.set_pose(sapien.core.Pose(p=[0, 0, 0.5]))


    # Add some lights so that you can observe the scene
    # game.scene.set_ambient_light([0.5, 0.5, 0.5])
    # game.scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    # viewer = sapien.utils.Viewer(game.renderer)  # Create a viewer (window)
    # viewer.set_scene(game.scene)  # Bind the viewer and the scene

    # # The coordinate frame in Sapien is: x(forward), y(left), z(upward)
    # # The principle axis of the camera is the x-axis
    # viewer.set_camera_xyz(x=-4, y=0, z=2)
    # # The rotation of the free camera is represented as [roll(x), pitch(-y), yaw(-z)]
    # # The camera now looks at the origin
    # viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)
    # viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

    # while not game.viewer.closed:  # Press key q to quit
    #     game.scene.step()  # Simulate the world
    #     game.scene.update_render()  # Update the world to the renderer
    #     game.viewer.render()


if __name__ == '__main__':
    main()
