


class SceneHistory():

    def __init__(self, scene):
        self.scene = scene
        self.val = 'Something'
        self.history_stake = []
        self.history_current_step = -1
        self.history_limit = 5

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

        return desc

    def restoreHistoryStamp(self, history_stamp):
        print('clearHistory')
        print('restoreHistoryStamp: ', history_stamp)




