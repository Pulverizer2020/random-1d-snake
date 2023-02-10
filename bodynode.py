import numpy as np
import numpy as np
import pyrosim.pyrosim as pyrosim

import queue



rootx = -3
rooty = 0
rootz = 2.5

build_body_array = []
build_brain_array = []

class COUNTER:
    def __init__(self):
        self.count = 0 # the root node always has node_id == 0
    
    def Get_Unique_Id(self):
        unique_id = self.count
        self.count += 1
        return unique_id

body_counter = COUNTER()
brain_counter = COUNTER()


class BODY_NODE:
    def __init__(self, outgoing_edges: list["BODY_EDGE"], recursive_limit: int ) -> None:
        # all body parts are rectangular prisims
        self.length = np.random.rand() * 2
        self.width = np.random.rand() * 2
        self.height = np.random.rand() * 2
        self.joint_type = "revolute"

        print("self.length, self.width, self.height", self.length, self.width, self.height)

        # recursive limit only affects how many times this node follows itself, not the other edges
        self.recursive_limit = recursive_limit
        self.outgoing_edges = outgoing_edges

    def Recursively_Generate_Body(self, parent: "BODY_NODE", parent_node_id: int | None):
        print("generating!")
        # give this root
        my_node_id = body_counter.Get_Unique_Id()


        my_new_length = np.random.uniform(low=0.2, high=1.5)
        my_new_width = np.random.uniform(low=0.2, high=1.5)
        my_new_height = np.random.uniform(low=0.2, high=1.5)
        print(my_new_height)

        has_sensor = np.random.rand() > 0.5 # has sensor 50% of the time, randomly
        if has_sensor:
            my_rgba_color = "0 1 0 1" # green
        else:
            my_rgba_color = "0 1 1 1" # cyan

        # Generate this node
        if my_node_id == 0:
            print("root node!")
            build_body_array.append(( 
                pyrosim.Send_Cube, 
                str(my_node_id),
                [rootx,rooty,rootz], 
                [my_new_length, my_new_width, my_new_height],
                my_rgba_color
            ))
            # pyrosim.Send_Cube(name=f"{my_node_id}", pos=[rootx,rooty,rootz] , size=[self.length, self.width, self.height])
        else:
            if parent_node_id == 0:
                # if parent node is the root node, do absolute positioning for joint
                build_body_array.append(( 
                    pyrosim.Send_Joint,
                    f"{parent_node_id}_{my_node_id}",
                    str(parent_node_id), 
                    str(my_node_id),
                    "revolute",
                    [rootx + parent.length/2, rooty, rootz],
                    "0 0 1"
                ))
                # pyrosim.Send_Joint(name=f"{parent_node_id}_{my_node_id}", parent=str(parent_node_id), child=str(my_node_id), type="revolute", position=[rootx + parent.length/2, rooty, rootz], jointAxis="0 0 1")
                pass
            else:
                # else, do relative positioning for joint
                build_body_array.append(( 
                    pyrosim.Send_Joint,
                    f"{parent_node_id}_{my_node_id}",
                    str(parent_node_id), 
                    str(my_node_id),
                    "revolute",
                    [parent.length, 0, 0],
                    "0 0 1"
                ))
                # pyrosim.Send_Joint(name=f"{parent_node_id}_{my_node_id}", parent=str(parent_node_id), child=str(my_node_id), type="revolute", position=[parent.length/2, 0, 0], jointAxis="0 0 1")
                pass
            
            # then create the body part
            # BECAUSE THIS IS A 1D SNAKE, I WILL JUST PLACE JOINT AND NEW NODE TO THE +X SIDE
            build_body_array.append(( 
                pyrosim.Send_Cube, 
                str(my_node_id),
                [my_new_length/2, 0, 0], 
                [my_new_length, my_new_width, my_new_height],
                my_rgba_color
            ))


            # create a motor neuron for every joint
            my_motor_id = brain_counter.Get_Unique_Id()
            build_brain_array.append((
                pyrosim.Send_Motor_Neuron,
                str(my_motor_id),
                f"{parent_node_id}_{my_node_id}"
            ))



        self.length = my_new_length
        self.width = my_new_width
        self.height = my_new_height


        if has_sensor:
            my_sensor_id = brain_counter.Get_Unique_Id()
            print("adding sensor!", my_sensor_id, my_node_id)
            
            build_brain_array.append((
                pyrosim.Send_Sensor_Neuron,
                str(my_sensor_id),
                str(my_node_id),
            ))


        # then follow outgoing edges
        for outgoing_edge in self.outgoing_edges:
            if outgoing_edge.child == "is_recursive":
                self.recursive_limit -= 1
                outgoing_edge.Follow_Edge(parent=self, parent_node_id=my_node_id)
            else:
                # generate that child without decrementing self.recursive_limit
                pass