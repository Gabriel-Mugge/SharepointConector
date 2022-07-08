
import os
import shutil
import tempfile
from scipy.sparse import lil_matrix
import numpy as np
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from treelib import Node, Tree
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



class ConectorSharepoint():
  
  def __init__(self, usuario, senha, url_site):
    self.site_url = url_site
    self.ctx = ClientContext(self.site_url).with_credentials(UserCredential(usuario, senha))
    self.raiz_sharepoint = os.path.basename(self.site_url)
    
    self.diretorios = []
    self.arquivos = []
    items = self.ctx.web.lists.get_by_title("Documents").items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get().execute_query()
    for item in items:  
      if item.file_system_object_type == 1:
        self.diretorios.append(item.folder.serverRelativeUrl.replace(f"/teams/{self.raiz_sharepoint}/Shared Documents/", ""))
      else:
        self.arquivos.append(item.file.serverRelativeUrl.replace(f"/teams/{self.raiz_sharepoint}/Shared Documents/", ""))
        
    self.tree = Tree()
    self.tree.create_node("Documentos", "raiz")  # root node

    aux_caminhos = []
    items = self.diretorios + self.arquivos
    for item in items:
      aux_caminhos.append(item.split('/'))

    for caminho in aux_caminhos:
      aux_concat = "raiz"
      apenas_um = True
      for indice in range(len(caminho) - 1):
        apenas_um = False
        if indice == 0:
          aux_concat += "/" + caminho[indice] + "/" + caminho[indice + 1]
        else:
          aux_concat += "/" + caminho[indice + 1]
        
        aux_concat_aux = "/".join(aux_concat.split('/')[0:-1])
        aux_concat_aux_aux = "/".join(aux_concat_aux.split('/')[0:-1])

        if self.tree.get_node(aux_concat_aux) != None: 
          filhos = [filho.tag for filho in self.tree.children(aux_concat_aux)]
        else:
            filhos = []

        
        if self.tree.get_node(aux_concat_aux) == None: 
          self.tree.create_node(caminho[indice], aux_concat_aux, parent=aux_concat_aux_aux)

        if not caminho[indice + 1] in filhos and self.tree.get_node(aux_concat) == None:
          self.tree.create_node(caminho[indice + 1], aux_concat, parent=aux_concat_aux)


      if apenas_um:
        self.tree.create_node(caminho[0], f'raiz/{caminho[0]}', parent=f'raiz')
        
        
      
        
        
    '''aux_caminhos = []
    self.index_graph_all_paths = []
    for item in items:
      item_split = item.split('/')
      aux_caminhos.append(item_split)
      for parcela in item_split:
        if parcela not in self.index_graph_all_paths:
          self.index_graph_all_paths.append(parcela)


    tam = len(self.index_graph_all_paths)
    self.grafo = lil_matrix((tam, tam), dtype=np.uint8)


    for caminho in aux_caminhos:
      for i in range(0, len(caminho) - 1): 
          indice_de = self.index_graph_all_paths.index(caminho[i])
          indice_para = self.index_graph_all_paths.index(caminho[i + 1])
          self.grafo[indice_de, indice_para] = 1'''
    
  
  def salvar_sharepoint(self, caminho_bricks, caminho_sharepoint, overwrite=False):
    
    if overwrite == False and self.path_exists(caminho_sharepoint):
      raise Exception("O Caminho no sharepoint já existe, caso queira sobrescreever o mesmo passe o parametro overwrite=True")
    else:
      with open(caminho_bricks, 'rb') as conteudo_binario:
        arquivo_binario = conteudo_binario.read()

      caminho_sharepoint = f'Shared Documents/{caminho_sharepoint}'
      nome_arquivo_salvar =  os.path.basename(caminho_bricks)
      self.ctx.web.get_folder_by_server_relative_url(caminho_sharepoint).upload_file(nome_arquivo_salvar, arquivo_binario).execute_query()
    
  
  def salvar_bricks(self, caminho_bricks, caminho_sharepoint, overwrite=False):
    
    if overwrite == False and self.os.path.exists(caminho_bricks):
      raise Exception("O Caminho no DataBricks já existe, caso queira sobrescreever o mesmo passe o parametro overwrite=True")
    else:
      caminho_sharepoint = f"/teams/{self.raiz_sharepoint}/Shared Documents/{caminho_sharepoint}"
      pasta_temporaria = tempfile.mkdtemp()
      nome_arquivo_capturar = os.path.basename(caminho_sharepoint)
      download_path = os.path.join(pasta_temporaria, nome_arquivo_capturar)

      with open(download_path, "wb") as local_file:
        self.ctx.web.get_file_by_server_relative_path(caminho_sharepoint).download(local_file).execute_query()

      origem = f"{pasta_temporaria}/{nome_arquivo_capturar}"
      destino = caminho_bricks
      shutil.move(origem, destino)
      shutil.rmtree(pasta_temporaria)
    
  
  def path_exists(self, caminho):
    if caminho in self.diretorios or caminho in self.arquivos:
      return True
    
    return False
  
  
  def list_dir(self, caminho, deep = False):
    caminho = caminho.split('/')[-1]

    lista_items = []
    if not deep:
      linha = list(self.grafo.getrow(self.index_graph_all_paths.index(caminho)).nonzero()[0])
      coluna = list(self.grafo.getrow(self.index_graph_all_paths.index(caminho)).nonzero()[1])

      for i in range(len(linha)):
        lista_items.append(self.index_graph_all_paths[coluna[i]])
    else:
      #fazer a busca em profundidade quando sobrar tempo
      #mais dificil pois provavelmnete vai tq ter recursão
      pass

    return lista_items
  
  def mostrar_arvore_diretorio(self, caminho=None, deep=True):
    if caminho == None and deep == True:
      self.tree.show()
      return

  def call_the_mika(self):
    img = mpimg.imread('mikoso.jpeg')
    imgplot = plt.imshow(img)
    plt.show()
    plt.close()
    
