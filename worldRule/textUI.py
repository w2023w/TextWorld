# _*_ coding:utf-8 _*_

import os, time, math

os.system('')


class Window:
	"""文字图形界面模块"""
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.prerender_set = []
		self.rendered = []
		
		self.init_render()
		
	def __str__(self): 
		"""编制默认信息"""
		return f"""
    规格：{self.width}×{self.height}
    样式：
        背景：{self.base_symbol}
        边型：{self.sides_symbol}
    描述：这是一个完全由文本字符构成的UI界面。
		"""
	def init_render(self): 
		"""初始化"""
		self.add({'type': 'floor', 'id': '00', 'z': 0, 'symbol': '·'})
		self.add({'type': 'reck', 'id': '01', 'x':0, 'y': 0, 'z': 0, 'width': self.width, 'height': self.height, 'fill': False, 'symbol': {'top': "—", 'right': '丨', 'bottom': '—', 'left': '丨', 'fill':'一'}})

		self.render()


	def reset_size(size, width=40, height=30): 
		"""重置窗口大小"""
		self.width = width
		self.height = height
		self.show()

	def add(self, obj):  
		"""添加图层及对象"""
		z_index = obj['z']
		if z_index > len(self.prerender_set) - 1:
			delta = z_index - len(self.prerender_set) + 1
			for i in range(delta):
				self.prerender_set.append([])
		self.prerender_set[z_index].append(obj)

	def destroy(self, oid, mod = 1):
		"""清除指定对象或图层"""
		if mod == 0:
			i = int(oid)
			if i > len(self.prerender_set) - 1:
				return
			self.prerender_set[i] = []
			self.show()
		elif mod == 1:
			i = oid[0]
			i = int(i)
			for j in range(len(self.prerender_set[i])):
				if oid == self.prerender_set[i][j]['id']:
					self.prerender_set[i].pop(j)
					break
			self.show()


	def render_floor(self, symbol): 
		"""渲染基底背景"""
		for m in range(self.height):
			line =  symbol * self.width
			self.rendered.append(line)

	def render_reck(self, x, y, width, height, borders, fill=False): 
		"""渲染矩形"""
		if x < 0:
			x = 0
		if y < 0:
			y = 0
		if x >= self.width:
			x = self.width - width - 1
		if y >= self.height:
			y = self.height - height - 1
			
		if width + x > self.width:
			width = self.width - x
		if height + y > self.height:
			height = self.height - y
		start_h = x
		end_h = x + width - 1
		start_v = y
		end_v = y + height - 1
		
		self.render_line(borders['top'], x, y, width, 0)
		self.render_line(borders['bottom'], x, y+height-1, width, 0)
		self.render_line(borders['left'], x, y, height, None)
		self.render_line(borders['right'], x+width-1, y, height, None)

		if fill:
			for m in range(height-2):
				self.render_fill(x+1, m+y+1, width-2, borders['fill'])

	def render_fill(self, x, y, long, symbol): 
		"""填充渲染"""
		self.render_line(symbol, x, y, long, 0)

	def render_point(self, x, y, symbol): 
		"""渲染点"""
		if x < 0:
			x = 0
		if y < 0:
			y = 0
		if x >= self.width:
			x = self.width - 1
		if y >= self.height:
			y = self.height - 1
		line = self.rendered[y]
		self.rendered[y] = f"{line[:x]}{symbol}{line[x+1:]}"

	def render_line(self, symbol, x, y, long, k): 
		"""渲染直线"""
		match k:
			case 0:
				'''水平直线'''
				if x + long > self.width:
					long = self.width - x
				string =self.rendered[y]
				self.rendered[y] = f'{string[:x]}' + f'{symbol}'*(long) + f'{string[x+long:]}'
			case None:
				'''垂直线'''
				if y + long > self.height:
					long = self.height - y
				for i in range(long):
					string =self.rendered[y+i]
					self.rendered[y+i] = f"{string[:x]}{symbol}{string[x+1:]}"
			case __:
				'''任意非水平非垂直的直线'''
				a = math.atan(k)
				delta_x = int(long * math.cos(a))
				for x2 in range(delta_x):
					self.render_point(x+x2, y+int(x2*k), symbol)

	def render(self, z_index=0): 
		"""全渲染成字符串列表"""
		if z_index > len(self.prerender_set) or z_index == 0:
			z_index=len(self.prerender_set)
			
		self.rendered = []
		index = z_index
		for i in range(index):
			index2 = len(self.prerender_set[i])
			for j in range(index2):
				p = self.prerender_set[i][j]
				match p['type']:
					case 'floor':
						self.render_floor(p['symbol'])
					case 'reck':
						self.render_reck(p['x'], p['y'], p['width'], p['height'], p['symbol'], p['fill'])
					case 'point':
						self.render_point(p['x'], p['y'], p['symbol'])
					case 'line':
						self.render_line(p['symbol'], p['x'], p['y'], p['l'], p['k'])
		self.show()

	def show(self): 
		"""展示渲染结果"""
		self.goback()
		for line in self.rendered:
			print('\t' + line)

	def goback(self):
		'''回退到起点'''
		print(f'\033[{self.height}A', end='')


if __name__ == "__main__":
	width = 40
	height = 30
	window = Window(width, height)

	window.add({'type': 'reck', 'id': '10', 'x':12, 'y': 10, 'z': 1, 'width': 25, 'height': 15, 'fill': True, 'symbol': {'top': "墙", 'right': '墙', 'bottom': '墙', 'left': '墙', 'fill': '艹'}})
	time.sleep(1)
	window.render()
	window.add({'type': 'line', 'id': '11', 'x':5, 'y': 5, 'z': 1, 'l': 20, 'k': None, 'symbol': '纵'})
	time.sleep(1)
	window.render()
	window.add({'type': 'line', 'id': '12', 'x':5, 'y': 5, 'z': 1, 'l': 30, 'k': 0, 'symbol': '横'})
	time.sleep(1)
	window.render()
	window.add({'type': 'line', 'id': '12', 'x':5, 'y': 5, 'z': 1, 'l': 30, 'k': 1, 'symbol': '线'})
	time.sleep(1)
	window.render()
	window.add({'type': 'point', 'id': '13', 'x':19, 'y': 14, 'z': 1, 'symbol': '我'})
	time.sleep(1)
	window.render()
	window.destroy('10')
	time.sleep(1)
	window.render()
	
	x0 = 19
	y0 = 14
	r = 12
	s = 17
	for t in range(s):
		rad = (2*math.pi/s)*t + 0*math.pi
		x = math.cos(rad) * r
		y = math.sin(rad) * r
		window.add({'type': 'point', 'id': f'1{4+t}', 'x': x0+int(x), 'y': y0+int(y), 'z': 1, 'symbol': '〇'})
		window.render()
		time.sleep(1)
		window.destroy(f'1{4+t}')
	os.system('pause')
		
		
