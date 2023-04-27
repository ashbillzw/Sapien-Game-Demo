import numpy

import sapien

class Table(object):
    def __init__(self, scene):
        self.scene = scene

        self.DEBUG = True

        self._build_table()

    def _build_table(self):
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
            limits= [[-1.5708, 1.5708]],
            pose_in_parent= sapien.core.Pose([0, 0, 0], [0.7071068, 0, 0, 0.7071068])
        )
        table_pitch_axle.add_box_collision(half_size=[1, 1, 4])
        if self.DEBUG: table_pitch_axle.add_box_visual(
            half_size= [1, 1, 4],
            color= [0, 1, 0]
        )

        table_roll_axle = table_builder.create_link_builder(table_pitch_axle)
        table_roll_axle.set_name("Table Roll Axle")
        table_roll_axle.set_joint_name("Table Roll Axle Bearing")
        table_roll_axle.set_joint_properties(
            joint_type= "revolute",
            limits= [[-1.5708, 1.5708]],
            pose_in_parent= sapien.core.Pose([0, 0, 0], [0.7071068, 0, 0, 0.7071068])
        )
        table_roll_axle.add_box_collision(half_size=[4, 4, 1])
        if self.DEBUG: table_roll_axle.add_box_visual(
            half_size= [4, 4, 1],
            color= [0, 0, 1]
        )

        self.articulation = table_builder.build(fix_root_link = True)
        self.articulation.set_name("Table")

        self.testpitchaxlejoint = [joint for joint in self.articulation.get_joints() if joint.name == "Table Pitch Axle Bearing"][0]
        self.testpitchaxlejoint.set_drive_property(stiffness=100000.0, damping=1000000.0)

        self.testrollaxlejoint = [joint for joint in self.articulation.get_joints() if joint.name == "Table Roll Axle Bearing"][0]
        self.testrollaxlejoint.set_drive_property(stiffness=100000.0, damping=1000000.0)
