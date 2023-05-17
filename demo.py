import robtiq_gripper_mdbsrtu as GRP
import serial.tools.list_ports

#author      ：王海峰 pluto Wang plutohfw@gmail.com
#creat edate ： 2023/05/16
#参考资料    ：https://robotiq.com/support

def serial_ports(): #自动寻找端口
    ports = list(serial.tools.list_ports.comports())  
    for port_no, description, address in ports:
        if 'USB' in description:
            return port_no
        
class CtrlGrp():
    def __init__(self,portname):
        self.grp=GRP.Gripper(portname)
    
    def ACT(self): #激活夹爪
        self.grp.ClearrACT()
        self.grp.activate()
        while not self.isACTed():
            None
        print('Gripper is activaited')

    def isACTed(self): #夹爪是否被激活
        while not self.grp.isavtivated():
            None
        return self.grp.isavtivated()
                
    def GTO(self,PosSpdFrc): #执行动作
        self.grp.grip(PosSpdFrc)    #[POS,SPEED,SPEED],open=full ,close=0
        while self.OBJ()[0] == 0x39: #0x39=57
            None            
        print('Completed',' Position：%3s/255 %5smm'%(self.OBJ()[1],self.OBJ()[2]))

    def OBJ(self): #返回当前值
        return self.grp.ReadGripperStatus()
    
    def SerClose(self): #关闭串口
        self.grp.serclose()
    
CtrGrp=CtrlGrp(serial_ports())
CtrGrp.ACT()
while 1:
    CtrGrp.GTO([0x00,0xFF,0x00])
    CtrGrp.GTO([0xFF,0xFF,0x00])
    CtrGrp.GTO([0x64,0xFF,0x00])
    CtrGrp.GTO([0xFF,0x64,0x00])
    CtrGrp.GTO([0x00,0x00,0x00])
    CtrGrp.GTO([0xFF,0x00,0x00])
