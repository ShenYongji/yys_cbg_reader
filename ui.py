from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
import cbgreader

class cbgui:
    def __init__(self):
        qfile = QFile("YYSCBGUI.ui")
        qfile.open(qfile.ReadOnly)
        qfile.close()
        self.cbgfunction = cbgreader.cbg()
        
        self.ui = QUiLoader().load(qfile)

        self.ui.Tojson.setEnabled(False)
        self.ui.Search.clicked.connect(self.search_button)
        self.ui.Delete.clicked.connect(self.delete_button)
        self.ui.Tojson.clicked.connect(self.tojson_button)

    def search_button(self):
        print("search button clicked")
        #cbgfunction = cbgreader.cbg()
        cbg_link = self.ui.cbgurl.text()
        print(cbg_link)
        self.ui.Notification.clear()
        self.soul_list = []
        var = ''
        if cbg_link == '':
            self.ui.Notification.setText("请输入藏宝阁的网页地址")
        else:
            #self.ui.Tojson.setEnabled(True)
            flag = self.cbgfunction.readurl(cbg_link)
            if len(flag) == 2:
                if flag[0] == 0:
                    self.ui.Notification.setText(flag[1])
                elif flag[0] == -1:
                    self.ui.Notification.setText("藏宝阁的网页地址无效，请重新输入")
                else:
                    self.ui.Tojson.setEnabled(True)
                    print("Loading name and server")
                    self.soul_list = flag[1]
                    self.cbgfunction.get_server_name(self.soul_list)
                    self.cbgfunction.pull_soul(self.soul_list)
                    var = '游戏ID: '+self.cbgfunction.name+ '\n' + \
                          '游戏大区: ' +self.cbgfunction.server +'\n'+\
                          '御魂数量（+15）： ' +str(self.cbgfunction.count)+'\n'+\
                           '-'*100+'\n'
                    self.ui.Notification.setText(var)
                    speed_l = self.cbgfunction.check_soul_speed()
                    print(speed_l)
                    for i in range(len(speed_l)):
                        pos = i + 1
                        speed = speed_l[i][0]
                        qua = speed_l[i][1]
                        soul_name = speed_l[i][2]
                        #print(pos,speed,qua,soul_name)
                        if pos == 2:
                            if qua == 1: pass
                            elif qua == 2: pass
                            elif qua == 3:
                                main = 36.0
                                speed -= main
                            elif qua == 4:
                                main = 38.0
                                speed -= main
                            elif qua == 5:
                                main = 40.0
                                speed -= main
                            elif qua == 6:
                                main = 57.0
                                speed -= main
                            var += str(pos) + '号位最快为： '+ str(main) +'+' +str(round(speed,4)) +'，类型： '+str(qua)+'星'+soul_name +'\n'
                        else:
                            var += str(pos) + '号位最快为： '+ str(round(speed,4)) +'，类型： '+str(qua)+'星'+soul_name +'\n'
                    self.ui.Notification.setText(var)
                    #self.cbgfunction.pull_soul(flag[1])
            


    def delete_button(self): 
        print("delete button clicked")
        self.ui.cbgurl.clear()
        self.ui.Notification.clear()
        if self.ui.Tojson.isEnabled():
            self.ui.Tojson.setEnabled(False)

    def tojson_button(self): 
        print("tojson button clicked")
        self.cbgfunction.jsonfile()
        text = self.ui.Notification.toPlainText()
        text += '-'*100+'\n'+'导出json文件，文件名为'+self.cbgfunction.server+'_'+self.cbgfunction.name+'_from_cbg.json\n'
        self.ui.Notification.setText(text)

app = QApplication([])
app.setWindowIcon(QIcon('icon.jpg'))
cbgui = cbgui()
cbgui.ui.show()
app.exec_()