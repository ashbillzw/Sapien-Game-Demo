import numpy

from sapien.core import Pose

class Table(object):
    def __init__(self, scene):
        self.scene = scene

        self.DEBUG = True

        self.testmap = numpy.zeros((4, 4))

        self._build_table()

    def _build_table(self):
        table_builder = self.scene.create_articulation_builder()

        table_anchor = table_builder.create_link_builder()
        table_anchor.set_name("Table Anchor")
        if self.DEBUG: table_anchor.add_sphere_visual(
            radius = 1,
            color = [1, 0, 0]
        )
        
        table_pitch_axle = table_builder.create_link_builder(table_anchor)
        table_pitch_axle.set_name("Table Pitch Axle")
        table_pitch_axle.set_joint_name("Table Pitch Axle Bearing")
        table_pitch_axle.set_joint_properties(
            joint_type= "revolute",
            limits= [[-1.5708, 1.5708]],
            pose_in_parent= Pose([0, 0, 0], [0.7071068, 0, 0, 0.7071068])
        )
        table_pitch_axle.add_box_collision(half_size= [0.5, 0.5, 2])
        if self.DEBUG: table_pitch_axle.add_box_visual(
            half_size= [0.5, 0.5, 2],
            color= [0, 1, 0]
        )

        table_roll_axle = table_builder.create_link_builder(table_pitch_axle)
        table_roll_axle.set_name("Table Roll Axle")
        table_roll_axle.set_joint_name("Table Roll Axle Bearing")
        table_roll_axle.set_joint_properties(
            joint_type= "revolute",
            limits= [[-1.5708, 1.5708]],
            pose_in_parent= Pose((0, 0, 0), [-0.7071068, 0, 0, 0.7071068])
        )
        table_roll_axle.add_box_collision(half_size= [2, 2, 0.5])
        if self.DEBUG: table_roll_axle.add_box_visual(
            half_size= (2, 2, 0.5),
            color= [0, 0, 1]
        )
        
        # wall = table_builder.create_link_builder(table_roll_axle)
        # wall.set_name("Wall " + str((0, 0)))
        # wall.set_joint_name("Wall " + str((0, 0)) + "Joint")
        # wall.set_joint_properties(
        #     joint_type= "fixed",
        #     limits= (0, 0),
        #     pose_in_parent= Pose([5, 0, 0], (0, 0, 0, 1))
        # )
        # wall.add_box_collision(half_size= [0.125, 0.125, 0.125])
        # wall.add_box_visual(half_size= [0.125, 0.125, 0.125], color= (1, 1, 1))


        for y in self.testmap:
            for x in y:
                wall = table_builder.create_link_builder(table_roll_axle)
                wall.set_name("Wall " + str((x, y)))
                wall.set_joint_name("Wall " + str((x, y)) + "Joint")
                wall.set_joint_properties(
                    joint_type= "fixed",
                    limits= (0, 0),
                    pose_in_parent= Pose([x, y[0], 5], (0, 0, 0, 1))
                )
                wall.add_box_collision(half_size=[0.25, 0.25, 0.25])
                wall.add_box_visual(half_size=[0.25, 0.25, 0.25])

        self.articulation = table_builder.build(fix_root_link = True)
        self.articulation.set_name("Table")

        self.testpitchaxlejoint = [joint for joint in self.articulation.get_joints() if joint.name == "Table Pitch Axle Bearing"][0]
        self.testpitchaxlejoint.set_drive_property(stiffness=100000.0, damping=1000000.0)

        self.testrollaxlejoint = [joint for joint in self.articulation.get_joints() if joint.name == "Table Roll Axle Bearing"][0]
        self.testrollaxlejoint.set_drive_property(stiffness=100000.0, damping=1000000.0)
