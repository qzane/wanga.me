import numpy as np
import cv2
import os

from time import sleep
import pyautogui as p

p.PAUSE=0.001

global IMAGE_NAME,IMAGE
IMAGE_NAME = os.listdir('./image/')
IMAGE = {}
for name in IMAGE_NAME:
    IMAGE[name.replace('.png','').replace('.bmp','')]=cv2.imread('./image/%s'%name)
for i in IMAGE:
    if IMAGE[i].std(2).mean()<1:# gray Image
        IMAGE[i]=cv2.cvtColor(IMAGE[i],cv2.COLOR_BGR2GRAY) 
#################### global ######################
def get_dis(pa,pb):
    return ((pa[0]-pb[0])**2+(pa[1]-pb[1])**2)**0.5
def cv2_match(tmp,threshold=0.8,grayscale='auto'):
    if grayscale == 'auto':
        if len(tmp.shape)==2:
            grayscale=True
        else:
            grayscale=False
    q = p.screenshot()
    w = cv2.cvtColor(np.array(q), cv2.COLOR_RGB2BGR)
    if grayscale:
        w = cv2.cvtColor(w,cv2.COLOR_BGR2GRAY)        
        if len(tmp.shape)>=3:
            tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
    else:
        if len(tmp.shape)<3:
            tmp = cv2.cvtColor(tmp,cv2.COLOR_GRAY2BGR)
    res = cv2.matchTemplate(w,tmp,cv2.TM_CCOEFF_NORMED)
    res = np.where(res>threshold)
    dis = min(tmp.shape[:2])/2
    l = int(tmp.shape[1]/2)
    h = int(tmp.shape[0]/2)
    result = []
    for i in range(len(res[0])):
        pos = (res[1][i]+l,res[0][i]+h)
        flag = True
        for j in result:
            if get_dis(pos,j) < dis:
                flag=False
                break
        if flag:
            result.append(pos)
    return result
def show_match(tmp,threshold=0.8,grayscale='auto'):
    sleep(2)
    for i in cv2_match(tmp,threshold,grayscale):
        p.moveTo(i)
        sleep(1)
    p.moveTo(100,100)

def image_to_gray():
    import os,re,cv2
    files = os.listdir('./image/')
    for name in files:
        if re.search('0.',name):
            img = cv2.imread('./image/%s'%name)
            ii = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite('./image/%s'%name.replace('0',''),ii)

def on_news():
    try:
        while(len(cv2_match(IMAGE['ok']))>0 or len(cv2_match(IMAGE['news']))>0 or len(cv2_match(IMAGE['new']))>0):
            sleep(0.1)            
            ok = cv2_match(IMAGE['ok'])[0]
            p.click(ok,pause=0.1)
    except p.FailSafeException:
        raise
    except:
        pass
    
def get_xy(p1,p2,p3):
    xy = [0,0]
    xy[0]=(p3[0]-p1[0])/(p2[0]-p1[0])
    xy[1]=(p3[1]-p1[1])/(p2[1]-p1[1])
    return xy

def get_pos(p1,p2,xy):
    pos = [0,0]
    pos[0] = int(p1[0]+(p2[0]-p1[0])*xy[0])
    pos[1] = int(p1[1]+(p2[1]-p1[1])*xy[1])
    return pos
    
#######begin remove
global AttackPos 
AttackPos = [700,450]
ContinuePos = [710,720]
def attack():#使用match修改
    global AttackPos 
    sleep(2)
    p.click()
    #sleep(0.001)     
    p.moveTo(AttackPos[0],AttackPos[1])
    p.click(clicks=50)

def c_t(n=10):#使用match修改
    sleep(2)
    for i in range(n):
        sleep(0.2)
        try:
            attack()
        except p.FailSafeException:
            raise
        except:
            pass
        sleep(0.2)
        p.moveTo(ContinuePos[0],ContinuePos[1])
#######end remove       
        
def fight_force():
    on_news()
    sleep(0.01)
    p.moveTo(100,100)
    sleep(0.01)
    pos = cv2_match(IMAGE['fight_no_force'])
    if len(pos)>0:
        p.click(pos[0])
        sleep(0.01)
    else:
        return
        
def fight_rate():
    on_news()
    p.moveTo(100,100)
    sleep(0.01)
    begin = cv2_match(IMAGE['fight_rate'])[0]
    end = cv2_match(IMAGE['fight_slave'],0.5)[0]
    p.moveTo(begin)
    p.click()
    p.dragTo(end)
    
def fight_result():
    on_news()
    sleep(0.01)
    result = 'unknown'
    if len(cv2_match(IMAGE['defeat']))>0:
        result = 'defeat'
    if len(cv2_match(IMAGE['victory']))>0:
        result = 'victory'
    try:
        ok = cv2_match(IMAGE['ok'])[0]
        p.click(ok,pause=0.1)
    except p.FailSafeException:
        raise
    except:
        pass
    return result
    
def fight_attack():
    p.moveTo(100,100)
    sleep(1)
    fight_force()
    fight_rate()    
    on_news()
    sleep(0.01)
    p1 = cv2_match(IMAGE['fight_slave'],0.5)[0]
    p2 = cv2_match(IMAGE['fight_force'])[0]
    AttackPos=[0,0]
    AttackPos[0]=p1[0]+int((p2[0]-p1[0])*0.483)
    AttackPos[1]=p1[1]-int((p1[1]-p2[1])*0.547)
    while(1): 
        on_news()
        begin = cv2_match(IMAGE['fight_begin'])
        if len(begin)==0:
            continue
        else:
            begin = begin[0]
        p.moveTo(begin,pause=0.1)
        p.click(begin)
        p.moveTo(AttackPos)
        p.click(clicks=30,pause=0.1)
        res = fight_result()
        if(res=='defeat'):
            break
        elif(res=='victory'):
            continue
        else:
            p.moveTo(100,100)
            sleep(1)
            on_news()
            continue
    
    on_news()
    toHome = cv2_match(IMAGE['tohome'])[0]
    p.click(toHome)    
                
    #sleep(2)
    #p.click()
    #sleep(0.001)     
    p.moveTo(AttackPos[0],AttackPos[1])
    
##### fight end
    
##### home begin
HOME_L = {
    'man':(-0.115,0.644),
    'man_blood':(0.21206581352833637, 0.6467661691542289),
    'level':(0.46617915904936014, -0.2736318407960199),
    'units':[0.6654478976234004, -0.26865671641791045],
    'damage':[0.46617915904936014, -0.5422885572139303],
    'mine':[0.6727605118829981, -0.5522388059701493],
    'battle':[1.2797074954296161, -0.4701492537313433]
    }  
def home_upgrade():    
    on_news()
    p1 = cv2_match(IMAGE['home_glod_left'])[0]
    p2 = cv2_match(IMAGE['home_fist_right'])[0]
    p.click(get_pos(p1,p2,HOME_L['damage']),clicks=20,pause=0.3)
    p.click(get_pos(p1,p2,HOME_L['man_blood']),clicks=5,pause=0.2)
    p.click(get_pos(p1,p2,HOME_L['man']),clicks=50,pause=1)
    p.click(get_pos(p1,p2,HOME_L['mine']),clicks=10,pause=0.3)
    p.click(get_pos(p1,p2,HOME_L['units']),clicks=5,pause=0.2)
    p.click(get_pos(p1,p2,HOME_L['level']),clicks=5,pause=0.3)
    
    
def toBattle():
    on_news()
    p1 = cv2_match(IMAGE['home_glod_left'])[0]
    p2 = cv2_match(IMAGE['home_fist_right'])[0]
    p.click(get_pos(p1,p2,HOME_L['battle']),clicks=1)
    
            
def main():
    while(1):
        try:
            home_upgrade()
        except p.FailSafeException:
            raise
        except:
            pass
        try:
            toBattle()
        except p.FailSafeException:
            raise
        except:
            pass
        try:
            fight_attack()
        except p.FailSafeException:
            raise
        except:
            pass

if __name__ == '__main__':
    p.confirm('请一定记住，终止本程序的方法为强行移动鼠标到屏幕最左上角!')
    p.confirm('重要的事情说三遍:终止本程序的方法为强行移动鼠标到屏幕最左上角!')
    p.confirm('重要的事情说三遍:终止本程序的方法为强行移动鼠标到屏幕最左上角!')
    if p.confirm('现在请打开游戏，进入升级页面，然后点击ok')=='OK':
        main()