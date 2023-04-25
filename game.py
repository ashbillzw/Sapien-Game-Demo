import numpy as np

import sapien

import map_loader


def get_joints_dict(articulation: sapien.core.Articulation):
    joints = articulation.get_joints()
    joint_names =  [joint.name for joint in joints]
    assert len(joint_names) == len(set(joint_names))
    return {joint.name: joint for joint in joints}


class Game(object):
    def __init__(self, DEBUG= False):
        self.gametick = 0

        self.DEBUG = DEBUG

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
        self.scene.add_ground(altitude=-256)

        self.scene.set_ambient_light([0.5, 0.5, 0.5])
        self.scene.add_directional_light(
            direction = [0, 1, -1],
            color = [0.5, 0.5, 0.5]
        )

        table_builder = self.scene.create_articulation_builder()

        table_anchor = table_builder.create_link_builder()
        table_anchor.set_name("Table Anchor")
        if self.DEBUG: table_anchor.add_sphere_visual(
            radius = 2,
            color = [1, 0, 0]
        )
        
        table_pitch_axle = table_builder.create_link_builder(table_anchor)
        table_pitch_axle.set_name("Table Pitch Axle")
        table_pitch_axle.set_joint_name("Table Pitch Axle Bearing")
        table_pitch_axle.set_joint_properties(
            joint_type= "revolute",
            limits= [[-0.25, 0.25]],
        )
        if self.DEBUG: table_pitch_axle.add_box_visual(
            half_size= [1, 1, 4],
            color= [0, 1, 0]
        )

        table_roll_axle = table_builder.create_link_builder(table_pitch_axle)
        table_roll_axle.set_name("Table Roll Axle")
        table_roll_axle.set_joint_name("Table Roll Axle Bearing")
        table_roll_axle.set_joint_properties(
            joint_type= "revolute",
            limits= [[-0.25, 0.25]],
            pose_in_parent= sapien.core.Pose([0, 0, 0], [0, 0.7071068, 0, 0.7071068])
        )

        # if self.DEBUG: table_roll_axle.add_box_visual(
        #     half_size= [1, 1, 4],
        #     color= [0, 0, 1]
        # )

        self.table = table_builder.build_kinematic()
        self.table.set_name("Table")

        self.testpitchaxlejoint = [joint for joint in self.table.get_joints() if joint.name == "Table Pitch Axle"][0]
        self.testpitchaxlejoint.set_drive_property(stiffness=1000.0, damping=0.0)

    def init_camera(self):
        self.viewer.set_camera_xyz(-64, 0, 64)
        self.viewer.set_camera_rpy(0,-45, 0)
        self.viewer.window.set_camera_parameters(0.05, 100, 1)

    def update(self):
        self.scene.step()

        if self.gametick % 5 == 0:
            self.scene.update_render()
            self.viewer.render()

        if self.viewer.window.key_down('w'):
            self.testpitchaxlejoint.set_drive_velocity_target(5)
        if self.viewer.window.key_down('s'):
            self.testpitchaxlejoint.set_drive_velocity_target(-5)

        self.gametick += 1


def main():
    game = Game(DEBUG= True)

if __name__ == '__main__':
    main()
