# _*_ coding:utf-8 _*_

import os

os.system('')


class Background:
    def __init__(self, symbol="一"):
        self.z_index = 0
        self.symbol = symbol

    def __str__(self):
        return f"这是第{self.z_index+1}层的地板"
        
    def get_symbol(self):
        return self.symbol


class Wall:
    def __init__(self, x, y, z=1, i=0):
        self.id = i
        self.z_index = z
        self.symbol = "墙"
        self.x = x
        self.y = y

    def __str__(self):
        return f"这是墙"

    def get_symbol(self):
        return self.symbol


class Player:
    def __init__(self, x, y, z=1):
        self.z_index = 1
        self.symbol = "我"
        self.x = x
        self.y = y

    def get_symbol(self):
        return self.symbol


class  Scene:
    def __init__(self, name, w, h):
        self.id = name
        self.width = w
        self.height = h
        self.txtmap = {0:[]}
        self.rendered = ''
        self.objs = {}
        self.init_bg()

    def __str__(self):
        return f"这是一个名为 {self.name} 的场景"

    def init_bg(self, bg=Background()):
        for m in range(self.height):
            line = ""
            for n in range(self.width):
                line += bg.symbol
            self.txtmap[bg.z_index].append(line)
        self.rendering()
        
    def rendering(self):
        for line in self.txtmap[0]:
            self.rendered.append(line+'\n')

    def show(self):
        print(self.rendered)

    def put_obj(self, name, x, y):
        obj = globals()[name](x=x, y=y)
        try:
            a = len(self.txtmap[obj.z_index])
        except:
            self.txtmap[obj.z_index] = {}
        self.txtmap[obj.z_index][obj.x,obj.y] = obj.symbol
        
        try:
            self.objs[name].append(obj)
        except:
            self.objs[name] = []
            self.objs[name].append(obj)

    def update_scence(self, name, x, y):
        self.put_obj(name, x, y)

    def scence_editor(self):
        #os.system('cls')
        tolog(f"\n你进入了场景{self.name}。")
        self.show()
        while True:
            cmds = input(f"|>神>世界:{self.name}）").strip().split()
            #cls()
            cmd = cmds[0]
            argvs = cmds[1:]
            tolog(f'{cmds}', ty='输入')
            match cmd:
                case 'add':
                    self.add_scence()
                case 'q':
                    tolog(f"你离开了世界{self.name}！")
                    break
                case 'cls':
                    os.system(cmd)
                case __:
                    tolog('指令错误；\nq：回归神国\ncls：清屏\nadd：创建场景')


class World:
    def __init__(self, name):
        self.name = name
        self.scenes = {}

    def __str__(self):
        return f"这是一个名为 {self.name} 的世界"

    def show_scenes(self):
        try:
            for key, val in self.scenes.items():
                print(f'\t{key}：{val}')
        except:
            tolog("天地初生，这里空荡荡的")

    def door2scene(self, name):
        try:
            self.scenes[name].scenes_editor()
        except:
            tolog(f"场景{name}不存在或崩溃了", ty="警告")
            self.show_scenes()

    def creat_scene(self, w=30, h=30):
        i = str(len(self.scenes))
        self.scenes[i]  = Scene(i, w, h)
        globals()['tolog'](f"神创造了一个名为 {i} 场景！")

    def world_editor(self):
        #os.system('cls')
        tolog(f"\n你进入了名为{self.name}的世界。")
        self.show_scenes()
        while True:
            cmds = input(f"|>神>世界:{self.name}）").strip().split()
            #cls()
            cmd = cmds[0]
            argvs = cmds[1:]
            tolog(f'{cmds}', ty='输入')
            match cmd:
                case 'c':
                    self.creat_scene()
                case 'q':
                    tolog(f"你离开了世界{self.name}！")
                    break
                case 'cls':
                    os.system(cmd)
                case 'door':
                    self.door2scence(argvs[0])
                case __:
                    tolog('指令错误；\nq：回归神国\ncls：清屏\nadd：创建场景')



class God:
    def __init__(self,name='god'):
        self.name = name
        self.worlds = {}

    def creat_world(self):
        i = str(len(self.worlds))
        self.worlds[i]  = World(i)
        globals()['tolog'](f"尊贵的创世神{self.name}冕下创造了一个名为 {i} 世界！")

    def show_worlds(self):
        try:
            for key, val in self.worlds.items():
                print(f'\t{key}：{val}')
        except:
            tolog("天地未分，世界不存")

    def door2world(self, name):
        try:
            self.worlds[name].world_editor()
        except:
            tolog(f"世界{name}不存在或崩溃了", ty="警告")
            self.show_worlds()

    def start_working(self):
        #os.system('cls')
        tolog(f"\n欢迎尊贵的{self.name}冕下归来，文字世界有你更精彩！")
        while True:
            cmds = input(f"|>神:{self.name}）").strip().split()
            #cls()
            cmd = cmds[0]
            argvs = cmds[1:]
            tolog(f'{cmds}', ty="输入")
            match cmd:
                case 'c':
                    self.creat_world()
                case 'q':
                    tolog(f"恭送{self.name}冕下,文字世界期待你的再次青睐！")
                    break
                case 'sws':
                    self.show_worlds()
                case 'cls':
                    os.system(cmd)
                case 'door':
                    self.door2world(argvs[0])
                case __:
                    tolog('指令错误；\n\033[2Cq：回归神国\ncls：清屏\n\033[2Cc：创建世界')


def tolog(msg, ty=''):
        print(f"{ty}\t{msg}")

def cls():
    print('\033[1A\033[0J')


if __name__ == "__main__":
    god_name = input('冕下尊姓大名？\n>)').strip()
    #cls()
    god = God(god_name)
    god.start_working()

    # print('\033[15A', end='')  # cursor up 5 lines
    # print('\033[30C' + '我', end='')
    # print('\033[15B', end='') 
    # print('\r', end='')  	# cursor back to start
    # print('\033[0J', end='')  # erase from cursor to end
