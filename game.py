import numpy as np

import sapien

import maploader


class Game(object):
    def __init__(self):
        self.engine = sapien.core.Engine()
        self.renderer = sapien.core.SapienRenderer()

        self.engine.set_renderer(self.renderer)

        self.scene = self.engine.create_scene()
        self.scene.set_timestep(1 / 300.0)

def main():
    
    game = Game()

    # NOTE: How to build actors (rigid bodies) is elaborated in create_actors.py
    game.scene.add_ground(altitude=0)  # Add a ground
    actor_builder = game.scene.create_actor_builder()
    actor_builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
    actor_builder.add_box_visual(half_size=[0.5, 0.5, 0.5], color=[1., 0., 0.])
    box = actor_builder.build(name='box')  # Add a box
    box.set_pose(sapien.Pose(p=[0, 0, 0.5]))


    # Add some lights so that you can observe the scene
    game.scene.set_ambient_light([0.5, 0.5, 0.5])
    game.scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    viewer = sapien.utils.Viewer(game.renderer)  # Create a viewer (window)
    viewer.set_scene(game.scene)  # Bind the viewer and the scene

    # The coordinate frame in Sapien is: x(forward), y(left), z(upward)
    # The principle axis of the camera is the x-axis
    viewer.set_camera_xyz(x=-4, y=0, z=2)
    # The rotation of the free camera is represented as [roll(x), pitch(-y), yaw(-z)]
    # The camera now looks at the origin
    viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)
    viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

    while not viewer.closed:  # Press key q to quit
        game.scene.step()  # Simulate the world
        game.scene.update_render()  # Update the world to the renderer
        viewer.render()


if __name__ == '__main__':
    main()
