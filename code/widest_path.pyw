import networkx as nx
from networkx.algorithms import tree
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_graph_example(x):
	if x == 'Grafo 1':
		G.add_edges_from([('a', 'b', {'weight': 7}), ('a', 'c', {'weight': 9}), ('a', 'f', {'weight': 14}), ('b', 'c', {'weight': 10}), ('b', 'd', {'weight': 15}), ('c', 'd', {'weight': 11}), ('c', 'e', {'weight': 14}), ('c', 'f', {'weight': 2}), ('d', 'e', {'weight': 6}), ('e', 'f', {'weight': 9})])
	elif x == 'Grafo 2':
		G.add_edges_from([('a', 'b', {'weight': 22}), ('a', 'c', {'weight': 1}), ('b', 'c', {'weight': 20}), ('b', 'd', {'weight': 10}), ('b', 'e', {'weight': 6}), ('c', 'd', {'weight': 9}), ('c', 'f', {'weight': 2}), ('e', 'f', {'weight': 11}), ('e', 'g', {'weight': 5}), ('e', 'h', {'weight': 7}), ('f', 'h', {'weight': 3}), ('g', 'h', {'weight': 4})])
	elif x == 'Grafo 3':
		G.add_edges_from([('a', 'b', {'weight': 22}), ('a', 'c', {'weight': 9}), ('a', 'd', {'weight': 12}), ('b', 'c', {'weight': 35}), ('b', 'f', {'weight': 36}), ('b', 'h', {'weight': 34}), ('c', 'd', {'weight': 4}), ('c', 'e', {'weight': 65}), ('c', 'f', {'weight': 42}), ('d', 'e', {'weight': 33}), ('d', 'i', {'weight': 30}), ('e', 'f', {'weight': 18}), ('e', 'g', {'weight': 23}), ('f', 'g', {'weight': 39}), ('f', 'h', {'weight': 24}), ('g', 'h', {'weight': 25}), ('g', 'i', {'weight': 21}), ('h', 'i', {'weight': 19})])
	default_colors(G)

def default_colors(X):
	for i in G.nodes:
		X.nodes[i]['color'] = 'lightblue'
	for i,j in G.edges:
		X[i][j]['color'] = 'black'

def draw_graph(X):
	pos = nx.spring_layout(X, k=1, seed=4)
	node_color = nx.get_node_attributes(X, "color").values()
	edge_color = nx.get_edge_attributes(X, "color").values()
	nx.draw(X, pos, with_labels=True, node_color=node_color, edge_color=edge_color)
	labels = nx.get_edge_attributes(X,'weight')
	nx.draw_networkx_edge_labels(X,pos,edge_labels=labels)
	return plt.gcf()

def widest_path(s, t):
	default_colors(G)
	H = nx.Graph()
	H.add_nodes_from(G.nodes)
	H.add_edges_from(list(tree.maximum_spanning_edges(G, algorithm="kruskal", data=True)))
	try:
		path_nodes = nx.shortest_path(H, source=s, target=t)
		for i in path_nodes:
			G.nodes[i]['color'] = 'red'
		path_edges = list(nx.utils.pairwise(path_nodes))
		for i,j in path_edges:
			G[i][j]['color'] = 'red'
		window['no_path'].Update(visible=False)	
	except:
		window['no_path'].Update(visible=True)
	draw_graph(G)

def draw_figure(canvas, X):
	global figure_canvas_agg
	if figure_canvas_agg:
		figure_canvas_agg.get_tk_widget().forget()
		plt.close('all')
	figure_canvas_agg = FigureCanvasTkAgg(draw_graph(X), canvas)
	figure_canvas_agg.draw()
	figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)



  
  
sg.theme('LightBlue3')

menu1 = [[sg.Text('Widest Path', font='Helvetica 11 bold')],
		 [sg.Text('\nO problema do caminho mais largo\n(widest path) consiste em encontrar\num caminho entre dois vértices em\num grafo ponderado, maximizando o\npeso da aresta de peso mínimo no\ncaminho.\n\nVocê pode testar um de nossos\nexemplos ou inserir o seu\npróprio grafo.\n')],
		 [sg.Button('Exemplos', key='exemplos')],
		 [sg.Button('Grafo personalizado', key='custom')],
		 [sg.Button('Sair', key='sair')]]

menu2 = [[sg.Text('Selecione um dos grafos\npré-definidos:\n', size=(50,None))],
         [sg.Combo(['Grafo 1', 'Grafo 2', 'Grafo 3'], readonly=True, default_value='Grafo 1', enable_events = True, key='combo_exemplos')],
         [sg.Text()],
         [sg.Button(button_text='Confirmar', key='conf_exemplo'), sg.Button('Voltar', key='voltar_inicio')]]

menu3 = [[sg.Text('Selecione os vértices de origem e\ndestino do caminho.')],
		 [sg.Text('Vértice inicial:'),sg.Combo([], readonly=True, key='combo_vi', size=(5,None), auto_size_text = False)],
		 [sg.Text('Vértice final:  '),sg.Combo([], readonly=True, key='combo_vf', size=(5,None), auto_size_text = False)],
		 [sg.Text()],
		 [sg.Button('Calcular', key='calcular'), sg.Button('Voltar')],
		 [sg.Text('\n\nNão existe caminho entre os\ndois vértices.', key='no_path', font='Helvetica 11 bold', visible=False)]]

menu4 = [[sg.Text('Utilize as seções abaixo para criar\nseu grafo.\n')],
		 [sg.Text('Adicionar Vértices:', font='Helvetica 11 bold')],
		 [sg.Text('Nome:'), sg.Input(size=(5,1), enable_events=True, key='nome_vertice'), sg.Button('Adicionar', disabled=True, key='adicionar_vertice')],
		 [sg.Text('\nAdicionar Arestas:', font='Helvetica 11 bold')],
		 [sg.Text('Vértices:'), sg.Combo([], readonly=True, key='vertice1', size=(5,None), auto_size_text = False, disabled=True, enable_events = True), sg.Combo([], readonly=True, key='vertice2', size=(5,None), auto_size_text = False, disabled=True, enable_events = True)], 
		 [sg.Text('Peso:     '), sg.Input(size=(5,1), disabled=True, enable_events=True, key='peso'), sg.Button('Adicionar', disabled=True, key='adicionar_aresta')],
		 [sg.Text('\nRemover Vértices:', font='Helvetica 11 bold')],
		 [sg.Combo([], readonly=True, disabled=True, size=(5,None), auto_size_text = False, enable_events=True, key='vertice_r'), sg.Button('Remover', disabled=True, key='remover_vertice')],
		 [sg.Text('\nRemover Arestas:', font='Helvetica 11 bold')],
		 [sg.Combo([], readonly=True, disabled=True, enable_events=True, key='aresta_r', size=(13,None), auto_size_text = False), sg.Button('Remover', disabled=True, key='remover_aresta')],
		 [sg.Text('')],
		 [sg.Button('Confirmar', key='confirmar2'), sg.Button('Resetar', key='reset'), sg.Button('Voltar', key='voltar_inicio2')]]

plot = [[sg.Canvas(canvas= None, size=(640,480), background_color='white', key='canvas')]]

largura = 220
altura = 480
layout = [[sg.pin(sg.Column(menu1, size=(largura,altura), key='c1')), sg.pin(sg.Column(menu2, size=(largura,altura), visible=False, key='c2')), sg.pin(sg.Column(menu3, size=(largura,altura), visible=False, key='c3')), sg.pin(sg.Column(menu4, size=(largura,altura), visible=False, key='c4')), sg.pin(sg.Column(plot, key='plot'))]]
window = sg.Window('Widest Path', layout, finalize=True)

G = nx.Graph()
F = nx.Graph()
figure_canvas_agg = None
anterior = ''

while True:  # Event Loop
	event, values = window.read()

	if event == sg.WIN_CLOSED or event == 'sair':
		break

	if event == 'exemplos':
		window['c1'].Update(visible=False)
		window['c2'].Update(visible=True)	
		G = nx.Graph()
		create_graph_example(values['combo_exemplos'])
		draw_figure(window['canvas'].TKCanvas, G)

	if event == 'combo_exemplos':
		G = nx.Graph()
		create_graph_example(values['combo_exemplos'])
		draw_figure(window['canvas'].TKCanvas, G)

	if event == 'conf_exemplo':
		anterior = 'c2'
		nodes = list(G.nodes)
		nodes.sort()
		window['combo_vi'].Update(values=nodes, set_to_index=0)
		window['combo_vf'].Update(values=nodes, set_to_index=len(nodes)-1)
		window['c2'].Update(visible=False)
		window['c3'].Update(visible=True)

	if event == 'voltar_inicio' or event == 'voltar_inicio2':
		window['c2'].Update(visible=False)
		window['c4'].Update(visible=False)
		window['c1'].Update(visible=True)	
		G = nx.Graph()
		draw_figure(window['canvas'].TKCanvas, G)

	if event == 'custom':
		window['c1'].Update(visible=False)
		window['c4'].Update(visible=True)	
		draw_figure(window['canvas'].TKCanvas, F)

	if event == 'nome_vertice':
		if len(values['nome_vertice']) > 5:
			window['nome_vertice'].Update(value=values['nome_vertice'][0:5])
		if values['nome_vertice'] != '':
			window['adicionar_vertice'].Update(disabled=False)
		else:
			window['adicionar_vertice'].Update(disabled=True)

	if event == 'adicionar_vertice':
		F.add_node(values['nome_vertice'], color='lightblue')	
		draw_figure(window['canvas'].TKCanvas, F)
		nodes = list(F.nodes)
		nodes.sort()
		window['vertice1'].Update(values=nodes)
		window['vertice2'].Update(values=nodes)
		window['vertice_r'].Update(values=nodes)
		window['nome_vertice'].Update(value='')
		window['adicionar_vertice'].Update(disabled=True)
		window['vertice2'].Update(disabled=True)
		window['peso'].Update(disabled=True)
		if(len(nodes) == 1):
			window['vertice_r'].Update(readonly=True)
		elif(len(nodes) > 1):
			window['vertice1'].Update(readonly=True)

	if event == 'vertice1':
		nodes = list(F.nodes)
		nodes.remove(values['vertice1'])
		window['vertice2'].Update(values=nodes)
		window['vertice2'].Update(readonly=True)
		window['peso'].Update(disabled=True)
		window['peso'].Update(value='')
		window['adicionar_aresta'].Update(disabled=True)

	if event == 'vertice2':
		window['peso'].Update(disabled=False)

	if event == 'peso':
		peso = ''		
		for i in list(values['peso']):
			if(i.isdigit() or i == '.'):
				peso = peso +  i
		if len(peso) > 5:
			peso = peso[0:5]
		window['peso'].Update(value=peso)
		if values['peso'] != '':
			window['adicionar_aresta'].Update(disabled=False)
		else:
			window['adicionar_aresta'].Update(disabled=True)

	if event == 'adicionar_aresta':
		F.add_edge(values['vertice1'], values['vertice2'], weight=int(values['peso']), color='black')
		draw_figure(window['canvas'].TKCanvas, F)
		window['vertice1'].Update(value='')
		window['vertice2'].Update(value='')
		window['peso'].Update(value='')
		window['vertice2'].Update(disabled=True)
		window['peso'].Update(disabled=True)
		window['adicionar_aresta'].Update(disabled=True)
		window['aresta_r'].Update(readonly=True)
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		window['aresta_r'].Update(values=list(arestas))

	if event == 'vertice_r':
		if values['vertice_r'] != '':
			window['remover_vertice'].Update(disabled=False)
		else:
			window['remover_vertice'].Update(disabled=True)

	if event == 'remover_vertice':
		F.remove_node(values['vertice_r'])
		draw_figure(window['canvas'].TKCanvas, F)
		nodes = list(F.nodes)
		nodes.sort()
		window['vertice1'].Update(values=nodes)
		window['vertice2'].Update(values=nodes)
		window['vertice_r'].Update(values=nodes)
		window['vertice2'].Update(disabled=True)
		window['remover_vertice'].Update(disabled=True)
		if(len(nodes) == 0):
			window['vertice_r'].Update(disabled=True)
		if(len(nodes) < 2):
			window['vertice1'].Update(disabled=True)
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		window['aresta_r'].Update(values=list(arestas))
		window['remover_aresta'].Update(disabled=True)
		if(len(arestas) == 0):
			window['aresta_r'].Update(disabled=True)

	if event == 'aresta_r':
		if values['aresta_r'] != '':
			window['remover_aresta'].Update(disabled=False)
		else:
			window['remover_aresta'].Update(disabled=True)

	if event == 'remover_aresta':
		aresta = values['aresta_r'][1:-1]
		F.remove_edge(aresta.split(',')[0],aresta.split(',')[1])
		draw_figure(window['canvas'].TKCanvas, F)
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		window['aresta_r'].Update(values=list(arestas))
		window['remover_aresta'].Update(disabled=True)
		if(len(arestas) == 0):
			window['aresta_r'].Update(disabled=True)

	if event == 'confirmar2':
		anterior = 'c4'
		G = F
		nodes = list(G.nodes)
		nodes.sort()
		window['combo_vi'].Update(values=nodes, set_to_index=0)
		window['combo_vf'].Update(values=nodes, set_to_index=len(nodes)-1)
		window['c4'].Update(visible=False)
		window['c3'].Update(visible=True)

	if event == 'reset':
		F = nx.Graph()
		draw_figure(window['canvas'].TKCanvas, F)
		for i in ['nome_vertice', 'vertice1', 'vertice2', 'peso', 'vertice_r', 'aresta_r']:
			window[i].Update(value='')
		for i in ['adicionar_vertice', 'vertice1', 'vertice2', 'peso', 'adicionar_aresta', 'vertice_r', 'remover_vertice', 'aresta_r', 'remover_aresta']:
			window[i].Update(disabled=True)

	if event == 'calcular':
		widest_path(values['combo_vi'], values['combo_vf'])
		draw_figure(window['canvas'].TKCanvas, G)

	if event == 'Voltar':
		window['no_path'].Update(visible=False)
		window['c3'].Update(visible=False)
		window[anterior].Update(visible=True)
		default_colors(G)
		draw_figure(window['canvas'].TKCanvas, G)

window.close()






