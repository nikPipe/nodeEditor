from nodeEditor.node_edge import *


class SceneHistory():

    def __init__(self, scene):
        self.scene = scene
        self.val = 'Something'
        self.history_stake = []
        self.history_current_step = -1
        self.history_limit = 100

    def undo(self):
        print('undo')
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        print('redo')
        if self.history_current_step + 1 < len(self.history_stake):
            self.history_current_step += 1
            self.restoreHistory()

    def restoreHistory(self):
        print('restoreHistory.....current Step: ', self.history_current_step, '(%d)' % len(self.history_stake))
        self.restoreHistoryStamp(self.history_stake[self.history_current_step])

    def storeHistory(self, desc):
        print('storeHistoery: "%s" ' %(desc), 'restoreHistory.....current Step: ', self.history_current_step, '(%d)' % len(self.history_stake))
        if self.history_current_step +1 >= self.history_limit:
            self.history_stake = self.history_stake[1:]
            self.history_current_step -= 1

        #IF THE POINTER IS NOT AT THE END OF THE LIST, THEN WE NEED TO REMOVE ALL THE ELEMENTS AFTER THE POINTER
        if self.history_current_step + 1 < len(self.history_stake):
            self.history_stake = self.history_stake[:self.history_current_step + 1]

        hs = self.createHistoryStamp(desc)
        self.history_stake.append(hs)
        self.history_current_step += 1
        print('storeHistoery: "%s" ' %(desc), 'restoreHistory.....current Step: ', self.history_current_step, '(%d)' % len(self.history_stake))
        print('\n')


    def createHistoryStamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges': []

        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif isinstance(item, QDMGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)


        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj
        }

        return history_stamp

    def restoreHistoryStamp(self, history_stamp):
        print('clearHistory')
        print('restoreHistoryStamp: ', history_stamp['desc'])

        self.scene.deserialize(history_stamp['snapshot'])

        for each_id in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id == each_id:
                    edge.grEdge.setSelected(True)
                    break
        for node_id in history_stamp['selection']['nodes']:
            for node in self.scene.nodes:
                if node.id == node_id:
                    node.grNode.setSelected(True)
                    break




