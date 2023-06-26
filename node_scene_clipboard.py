from collections import OrderedDict

from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_edge import QDMGraphicsEdge
from nodeEditor.node_node import Node
from nodeEditor.node_edge import *


class SceneClipboard():
    def __init__(self, scene):
        '''
        :param scene:
        '''
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene


    def serializeSelected(self, delete=False):
        '''

        :param delete:
        :return:
        '''
        print('---- Copy to clipboard ----')
        sel = self.scene.grScene.selectedItems()
        sel_nodes, sel_edges, sel_socket = [], [], {}
        #SORT EDGES AND NODES
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in item.node.inputs + item.node.outputs:
                    sel_socket[socket.id] = socket
            elif isinstance(item, QDMGraphicsEdge):
                sel_edges.append(item.edge)




        #print('  Nodes:\n    ', sel_nodes)
        #print('  Edges:\n    ', sel_edges)
        #print('  Sockets:\n    ', sel_socket)

        #REMOVE ALL THE EDGES WHICH ARE NOT CONNECTED TO A NODE
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_socket and edge.end_socket.id in sel_socket:
                pass
            else:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            sel_edges.remove(edge)
        
        #MAKE FINA LIST OF EDGES
        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())
            
        data = OrderedDict()
        data['nodes'] = sel_nodes
        data['edges'] = edges_final

        # IF CUT WAS SELECTED, DELETE ALL THE SELECTED ITEMS
        if delete:
            self.scene.getView().deleteSelected()
            #store history
            self.scene.history.storeHistory('Cut out elements from scene')

        return data

    def deserializeFromClipboard(self, data):

        '''

        :return:
        '''
        print('SceneClipboard.deserializeFromClipboard()', data)
        hashmap = {}
        #CALCULATE MOUSE POSITION
        view = self.scene.getView()
        mouse_position = view.last_scene_mouse_position
        print('  Mouse position:', mouse_position.x(), mouse_position.y())

        #CALCULATE SELECTED OBJECT BBOX AND CONTENT
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y

        bbox_center_x = (min_x + max_x) / 2
        bbox_center_y = (min_y + max_y) / 2


        #CALCULATE OFFSET
        offset_x = mouse_position.x() - bbox_center_x
        offset_y = mouse_position.y() - bbox_center_y

        #CREATE NODES
        for node_data in data['nodes']:
            new_node = self.scene.getNodeClassFromData(node_data)(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)
            pos = new_node.pos
            new_node.setPos(pos.x() + offset_x, pos.y() + offset_y)


        #CREATE EDGES
        if 'edges' in data:
            for edge_data in data['edges']:

                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        #STORE HISTORY
        self.scene.history.storeHistory('Pasted elements on scene')