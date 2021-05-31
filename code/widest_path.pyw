import networkx as nx
from networkx.algorithms import tree
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Função para preencher o grafo com o exemplo escolhido
def create_graph_example(x):
	if x == 'Grafo 1':
		G.add_edges_from([('a', 'b', {'weight': 7}), ('a', 'c', {'weight': 9}), ('a', 'f', {'weight': 14}), ('b', 'c', {'weight': 10}), ('b', 'd', {'weight': 15}), ('c', 'd', {'weight': 11}), ('c', 'e', {'weight': 14}), ('c', 'f', {'weight': 2}), ('d', 'e', {'weight': 6}), ('e', 'f', {'weight': 9})])
	elif x == 'Grafo 2':
		G.add_edges_from([('a', 'b', {'weight': 22}), ('a', 'c', {'weight': 1}), ('b', 'c', {'weight': 20}), ('b', 'd', {'weight': 10}), ('b', 'e', {'weight': 6}), ('c', 'd', {'weight': 9}), ('c', 'f', {'weight': 2}), ('e', 'f', {'weight': 11}), ('e', 'g', {'weight': 5}), ('e', 'h', {'weight': 7}), ('f', 'h', {'weight': 3}), ('g', 'h', {'weight': 4})])
	elif x == 'Grafo 3':
		G.add_edges_from([('a', 'b', {'weight': 22}), ('a', 'c', {'weight': 9}), ('a', 'd', {'weight': 12}), ('b', 'c', {'weight': 35}), ('b', 'f', {'weight': 36}), ('b', 'h', {'weight': 34}), ('c', 'd', {'weight': 4}), ('c', 'e', {'weight': 65}), ('c', 'f', {'weight': 42}), ('d', 'e', {'weight': 33}), ('d', 'i', {'weight': 30}), ('e', 'f', {'weight': 18}), ('e', 'g', {'weight': 23}), ('f', 'g', {'weight': 39}), ('f', 'h', {'weight': 24}), ('g', 'h', {'weight': 25}), ('g', 'i', {'weight': 21}), ('h', 'i', {'weight': 19})])
	default_colors(G)

# Adiciona os atributos de cor para todos os vértices e arestas do grafo
def default_colors(X):
	for i in G.nodes:
		X.nodes[i]['color'] = 'lightblue'
	for i,j in G.edges:
		X[i][j]['color'] = 'black'

#Função para desenhar o grafo
def draw_graph(X):
	# Gera as posições do grafo, com tamanho mínimo de aresta k e uso de seed para que um dado grafo tenha sempre a mesma disposição
	pos = nx.spring_layout(X, k=1, seed=4)
	# Pega a lista de cores dos vértices e arestas para usar como atributo na função de desenho
	node_color = nx.get_node_attributes(X, "color").values()
	edge_color = nx.get_edge_attributes(X, "color").values()
	# Desenha os vértices com seus rótulos e as arestas
	nx.draw(X, pos, with_labels=True, node_color=node_color, edge_color=edge_color)
	# Lista dos pesos das arestas
	labels = nx.get_edge_attributes(X,'weight')
	# Inclui os pesos das arestas no desenho
	nx.draw_networkx_edge_labels(X,pos,edge_labels=labels)
	# Retorna uma imagem com o desenho do grafo
	return plt.gcf()

# Função para o cálculo do widest path, s -> vértice inicial, t -> vértice final
def widest_path(s, t):
	# Coloca as cores iniciais nos vértices e arestas
	default_colors(G)
	# Cria o grafo secundário
	H = nx.Graph()
	# Copia os vértices do grafo primário para o secundário
	H.add_nodes_from(G.nodes)
	# Gera a árvore geradora de peso maxizado no grafo secundário
	H.add_edges_from(list(tree.maximum_spanning_edges(G, algorithm="kruskal", data=True)))
	# Tenta gerar o caminho entre os dois vértices selecionados
	try:
		# Lista dos vértices pertencentes ao caminho entre 's' e 't' 
		path_nodes = nx.shortest_path(H, source=s, target=t)
		# Pinta os vértices do caminho de vermelho
		for i in path_nodes:
			G.nodes[i]['color'] = 'red'
		# Lista das arestas do caminho
		path_edges = list(nx.utils.pairwise(path_nodes))
		# Pinta as arestas do caminho de vermelho
		for i,j in path_edges:
			G[i][j]['color'] = 'red'
		window['no_path'].Update(visible=False)
	# Caso não consiga gerar o caminho exibe o aviso	
	except:
		window['no_path'].Update(visible=True)
	draw_graph(G)

# Função de ligação entre os objetos de desenho da interface gráfica e os objetos de desenho da biblioteca matploblib
def draw_figure(canvas, X):
	global figure_canvas_agg
	# Checa se já tem algo desenhado e se tiver limpa
	if figure_canvas_agg:
		figure_canvas_agg.get_tk_widget().forget()
		plt.close('all')
	figure_canvas_agg = FigureCanvasTkAgg(draw_graph(X), canvas)
	figure_canvas_agg.draw()
	figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


# Tema de cor da GUI
sg.theme('LightBlue3')

# Menu da tela inicial
menu1 = [[sg.Text('Widest Path', font='Helvetica 11 bold')],
		 [sg.Text('\nO problema do caminho mais largo\n(widest path) consiste em encontrar\num caminho entre dois vértices em\num grafo ponderado, maximizando o\npeso da aresta de peso mínimo no\ncaminho.\n\nVocê pode testar um de nossos\nexemplos ou inserir o seu\npróprio grafo.\n')],
		 [sg.Button('Exemplos', key='exemplos')],
		 [sg.Button('Grafo personalizado', key='custom')],
		 [sg.Button('Sair', key='sair')]]

# Menu da tela de exemplos
menu2 = [[sg.Text('Selecione um dos grafos\npré-definidos:\n', size=(50,None))],
         [sg.Combo(['Grafo 1', 'Grafo 2', 'Grafo 3'], readonly=True, default_value='Grafo 1', enable_events = True, key='combo_exemplos')],
         [sg.Text()],
         [sg.Button(button_text='Confirmar', key='conf_exemplo'), sg.Button('Voltar', key='voltar_inicio')]]

# Menu da tela de cálculo do widest path
menu3 = [[sg.Text('Selecione os vértices de origem e\ndestino do caminho.')],
		 [sg.Text('Vértice inicial:'),sg.Combo([], readonly=True, key='combo_vi', size=(5,None), auto_size_text = False)],
		 [sg.Text('Vértice final:  '),sg.Combo([], readonly=True, key='combo_vf', size=(5,None), auto_size_text = False)],
		 [sg.Text()],
		 [sg.Button('Calcular', key='calcular'), sg.Button('Voltar')],
		 [sg.Text('\n\nNão existe caminho entre os\ndois vértices.', key='no_path', font='Helvetica 11 bold', visible=False)]]

# Menu da tela de criação e edição do grafo
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

# Canvas de desenho do grafo
plot = [[sg.Canvas(canvas= None, size=(640,480), background_color='white', key='canvas')]]

#largura e altura do menu
largura = 220
altura = 480

#Layout da GUI
layout = [[sg.pin(sg.Column(menu1, size=(largura,altura), key='c1')), sg.pin(sg.Column(menu2, size=(largura,altura), visible=False, key='c2')), sg.pin(sg.Column(menu3, size=(largura,altura), visible=False, key='c3')), sg.pin(sg.Column(menu4, size=(largura,altura), visible=False, key='c4')), sg.pin(sg.Column(plot, key='plot'))]]
window = sg.Window('Widest Path', layout, finalize=True)

# Instancia o grafo primário
G = nx.Graph()
# Instancia o grafo auxiliar utilizado para a edição do grafo personalizado
F = nx.Graph()
figure_canvas_agg = None
# variável para guardar a tela anterior para retornar da tela de cálculo (exemplos ou grafo personalizado)
anterior = ''

#Loop de eventos da interface
while True:
	event, values = window.read()

	# Encerrar execução
	if event == sg.WIN_CLOSED or event == 'sair':
		break

	if event == 'exemplos':
		window['c1'].Update(visible=False)
		window['c2'].Update(visible=True)	
		
		G = nx.Graph()
		# Carrega o exemplo
		create_graph_example(values['combo_exemplos'])
		
		draw_figure(window['canvas'].TKCanvas, G)

	if event == 'combo_exemplos':
		# Reseta o grafo primário
		G = nx.Graph()
		# Reseta o grafo primário
		create_graph_example(values['combo_exemplos'])
		# Desenha o exemplo
		draw_figure(window['canvas'].TKCanvas, G)

	# Seleção de exemplo
	if event == 'conf_exemplo':
		# grava tela anterior
		anterior = 'c2'
		# lista de vértices do exemplos
		nodes = list(G.nodes)
		# ordena lista de vértices 
		nodes.sort()
		# alimenta as comboboxes com a lista de vértices
		window['combo_vi'].Update(values=nodes, set_to_index=0)
		window['combo_vf'].Update(values=nodes, set_to_index=len(nodes)-1)
		window['c2'].Update(visible=False)
		window['c3'].Update(visible=True)

	# Voltar para tela inicial
	if event == 'voltar_inicio' or event == 'voltar_inicio2':
		window['c2'].Update(visible=False)
		window['c4'].Update(visible=False)
		window['c1'].Update(visible=True)	
		# Reseta grafo
		G = nx.Graph()
		# Desenha grafo vazio
		draw_figure(window['canvas'].TKCanvas, G)

	# Entra na tela de grafo personalizado
	if event == 'custom':
		window['c1'].Update(visible=False)
		window['c4'].Update(visible=True)	
		# Desenha o grafo personalizado atual
		draw_figure(window['canvas'].TKCanvas, F)

	# Tratamento da entrada do nome do vértice, limita o número de caracteres para evitar poluir o desenho
	if event == 'nome_vertice':
		if len(values['nome_vertice']) > 5:
			window['nome_vertice'].Update(value=values['nome_vertice'][0:5])
		if values['nome_vertice'] != '':
			window['adicionar_vertice'].Update(disabled=False)
		else:
			window['adicionar_vertice'].Update(disabled=True)

	
	if event == 'adicionar_vertice':
		# Adiciona o vértice no grafo
		F.add_node(values['nome_vertice'], color='lightblue')	
		# Desenha o grafo com o novo vértice
		draw_figure(window['canvas'].TKCanvas, F)
		# Lista de vértices do grafo ordenada
		nodes = list(F.nodes)
		nodes.sort()
		# Alimenta as comboboxes com a lista de vértices do grafo
		window['vertice1'].Update(values=nodes)
		window['vertice2'].Update(values=nodes)
		window['vertice_r'].Update(values=nodes)
		window['nome_vertice'].Update(value='')
		window['adicionar_vertice'].Update(disabled=True)
		window['vertice2'].Update(disabled=True)
		window['peso'].Update(disabled=True)
		# desbloqueia a remoção de vértice
		if(len(nodes) == 1):
			window['vertice_r'].Update(readonly=True)
		# desbloqueia a adição de aresta
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
		# Tratamento da entrada do peso, só aceita digitos ou ponto
		for i in list(values['peso']):
			if(i.isdigit() or i == '.'):
				peso = peso +  i
		# Limita o peso em 5 digitos para não poluir o desenho
		if len(peso) > 5:
			peso = peso[0:5]
		window['peso'].Update(value=peso)
		if values['peso'] != '':
			window['adicionar_aresta'].Update(disabled=False)
		else:
			window['adicionar_aresta'].Update(disabled=True)

	if event == 'adicionar_aresta':
		# Adiciona a aresta do grafo
		F.add_edge(values['vertice1'], values['vertice2'], weight=int(values['peso']), color='black')
		# Desenha grafo com a nova aresta
		draw_figure(window['canvas'].TKCanvas, F)
		window['vertice1'].Update(value='')
		window['vertice2'].Update(value='')
		window['peso'].Update(value='')
		window['vertice2'].Update(disabled=True)
		window['peso'].Update(disabled=True)
		window['adicionar_aresta'].Update(disabled=True)
		window['aresta_r'].Update(readonly=True)
		# Gera a lista de arestas
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		# Alimenta a combobox com a lista de arestas
		window['aresta_r'].Update(values=list(arestas))

	if event == 'vertice_r':
		if values['vertice_r'] != '':
			window['remover_vertice'].Update(disabled=False)
		else:
			window['remover_vertice'].Update(disabled=True)

	if event == 'remover_vertice':
		# Remove o vértice do grafo
		F.remove_node(values['vertice_r'])
		# Desenha o grafo sem o vértice removido
		draw_figure(window['canvas'].TKCanvas, F)
		# Lista ordenada dos vértices
		nodes = list(F.nodes)
		nodes.sort()
		# Alimenta as comboboxes com a lista dos vértices
		window['vertice1'].Update(values=nodes)
		window['vertice2'].Update(values=nodes)
		window['vertice_r'].Update(values=nodes)
		window['vertice2'].Update(disabled=True)
		window['remover_vertice'].Update(disabled=True)
		if(len(nodes) == 0):
			window['vertice_r'].Update(disabled=True)
		if(len(nodes) < 2):
			window['vertice1'].Update(disabled=True)
		# Lista das arestas
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		# Alimenta a combobox com a lista das arestas
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
		# extrai os vértices da aresta
		aresta = values['aresta_r'][1:-1]
		# remove aresta do grafo
		F.remove_edge(aresta.split(',')[0],aresta.split(',')[1])
		# desenha o grafo sem a aresta removida
		draw_figure(window['canvas'].TKCanvas, F)
		# Lista das arestas
		arestas = []
		for i in list(F.edges):
			arestas.append('(' + i[0] + ',' + i[1] + ')')
		# Alimenta a combobox com a lista das arestas
		window['aresta_r'].Update(values=list(arestas))
		window['remover_aresta'].Update(disabled=True)
		if(len(arestas) == 0):
			window['aresta_r'].Update(disabled=True)

	if event == 'confirmar2':
		anterior = 'c4'
		# Copia o grafo auxiliar para o grafo primário
		G = F
		# Lista ordenada dos vértices
		nodes = list(G.nodes)
		nodes.sort()
		# Alimenta as comboboxes com a lista de vértices
		window['combo_vi'].Update(values=nodes, set_to_index=0)
		window['combo_vf'].Update(values=nodes, set_to_index=len(nodes)-1)
		window['c4'].Update(visible=False)
		window['c3'].Update(visible=True)

	if event == 'reset':
		# Reseta grafo auxiliar
		F = nx.Graph()
		# Desenha grafo vazio
		draw_figure(window['canvas'].TKCanvas, F)
		# Limpa todos os campos da tela de edição
		for i in ['nome_vertice', 'vertice1', 'vertice2', 'peso', 'vertice_r', 'aresta_r']:
			window[i].Update(value='')
		for i in ['adicionar_vertice', 'vertice1', 'vertice2', 'peso', 'adicionar_aresta', 'vertice_r', 'remover_vertice', 'aresta_r', 'remover_aresta']:
			window[i].Update(disabled=True)


	if event == 'calcular':
		# Cálcula o Widest Path
		widest_path(values['combo_vi'], values['combo_vf'])
		# Desenha o resultado
		draw_figure(window['canvas'].TKCanvas, G)

	# Volta para a tela anterior a tela de cálculo do caminho
	if event == 'Voltar':
		window['no_path'].Update(visible=False)
		window['c3'].Update(visible=False)
		window[anterior].Update(visible=True)
		# Reseta as cores do grafo
		default_colors(G)
		# Desenha o grafo com as cores iniciais
		draw_figure(window['canvas'].TKCanvas, G)

# Fecha janela do programa
window.close()





