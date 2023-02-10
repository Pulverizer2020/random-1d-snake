import numpy as np
from typing import Literal

from bodynode import BODY_NODE



class BODY_EDGE:
    def __init__(self, child: BODY_NODE | Literal["is_recursive"]) -> None:
        # all body parts are rectangular prisims
        # self.change_length = np.random.rand() / 5 
        # self.change_width = np.random.rand() / 5 
        # self.change_height = np.random.rand() / 5 

        self.child = child

    def Follow_Edge(self, parent: BODY_NODE, parent_node_id: int):
        if self.child == "is_recursive":
            if not parent.recursive_limit == 0:
                # parent.length += self.change_length
                # parent.width += self.change_width
                # parent.height += self.change_height
                parent.Recursively_Generate_Body(parent=parent, parent_node_id=parent_node_id)
        else:
            if not self.child.recursive_limit == 0:
                # change the child based on self.change_length etc, and then generate the body
                pass
      
    