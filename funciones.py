def FormarArbol(dic):
	tree = []
	for elem in dic["value"]:
		# Si el path es root entra en el elemento 0 de tree.
		if elem["parentReference"]["path"] == "/drive/root:":
			# Si La lista tree aún no tiene elementos crea el primero. 
			if len(tree) == 0:
				tree.append({})
			
			# Si hay una carpeta en el nivel,
			if "folder" in elem:
				# Y aún no existe el diccionario folders, lo crea y añade a la lista uno nuevo con el nombre de la carpeta.
				if "folders" not in tree[0]:
					tree[0]["folders"]=[]
					tree[0]["folders"].append(dict(name=elem["name"]))
				# si existe añade a la lista de folders un nuevo diccionario con el nombre de la carpeta.
				else:
					tree[0]["folders"].append(dict(name=elem["name"]))
				# si la carpeta tiene carpetas dentro:
				if elem["folder"]["childCount"] > 0:
					# Se recorren las carpetas que hay en el nivel 0
					for i in tree[0]["folders"]:
						# Cuando la carpeta sea la que estamos tratando,
						if i["name"] == elem["name"]:
							# Añade un nuevo valor al diccionario con formato: "NumCarpetas"= X
							i["childCount"]=elem["folder"]["childCount"]

			# Si hay un fichero en el nivel,
			if "file" in elem:
				# Y aún no existe el diccionario files, lo crea y añade a la lista uno nuevo con el nombre del fichero.
				if "files" not in tree[0]:
					tree[0]["files"]=[]
					tree[0]["files"].append(dict(name=elem["name"]))	
				# si existe añade a la lista de files un nuevo diccionario con el nombre del fichero.
				else:
					tree[0]["files"].append(dict(name=elem["name"]))
	return tree