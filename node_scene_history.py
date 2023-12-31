from nodeEditor.node_edge import *
from nodeEditor.utils import dumpException


class SceneHistory():

    def __init__(self, scene):
        self.scene = scene
        self.val = 'Something'
        self.clear()
        self.history_limit = 100

    def clear(self):
        self.history_stake = []
        self.history_current_step = -1

    def storeInitialHistoryStamp(self):
        self.storeHistory('Initial History Stamp')

    def canUndo(self):
        return self.history_current_step > 0

    def canRedo(self):
        return self.history_current_step + 1 < len(self.history_stake)

    def undo(self):
        print('undo')
        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        print('redo')
        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()

    def restoreHistory(self):
        self.restoreHistoryStamp(self.history_stake[self.history_current_step])

    def storeHistory(self, desc):
        if self.history_current_step +1 >= self.history_limit:
            self.history_stake = self.history_stake[1:]
            self.history_current_step -= 1

        #IF THE POINTER IS NOT AT THE END OF THE LIST, THEN WE NEED TO REMOVE ALL THE ELEMENTS AFTER THE POINTER
        if self.history_current_step + 1 < len(self.history_stake):
            self.history_stake = self.history_stake[:self.history_current_step + 1]

        hs = self.createHistoryStamp(desc)
        self.history_stake.append(hs)
        self.history_current_step += 1

        self.scene.hasBeenModified = True
        self.scene.parentSelf.setTitle_()


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

        self.scene.deserialize(history_stamp['snapshot'])
        try:
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
        except Exception as e:
            dumpException(e)




