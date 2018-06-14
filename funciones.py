def FormarArbol(dic,tree,subcarpetas):
	lvl=ObtenerNivel(dic["value"][0]["parentReference"]["path"])
	# Recorre los elementos del diccionario
	for elem in dic["value"]:
		# Si tree no tiene elementos añade un diccionario para el nivel 0. 
		if len(tree) == 0:
			tree.append({})
		# Si los elementos de tree -1 no corresponden con el nivel actual, añade un diccionario.
		elif len(tree)-1 != lvl:
			tree.append({})
		# Si subcarpetas no tiene elementos añade un diccionario para el nivel 0. 
		if len(subcarpetas) == 0:
			subcarpetas.append([])
		# Si los elementos de subcarpetas -1 no corresponden con el nivel actual, añade un diccionario.
		elif len(subcarpetas)-1 != lvl:
			subcarpetas.append([])

		# Si hay una carpeta en el nivel,
		if "folder" in elem:
			# Y aún no existe el diccionario folders, lo crea y añade a la lista el elemento actual.
			if "folders" not in tree[lvl]:
				tree[lvl]["folders"]=[]
				tree[lvl]["folders"].append(dict(name=elem["name"],parent=elem["parentReference"]["path"],id=elem["id"],web=elem["webUrl"]))
			# si existe añade a la lista de folders un nuevo diccionario con el nombre de la carpeta.
			else:
				tree[lvl]["folders"].append(dict(name=elem["name"],parent=elem["parentReference"]["path"],id=elem["id"],web=elem["webUrl"]))			# si la carpeta tiene carpetas dentro:
			if elem["folder"]["childCount"] > 0:
				# Añade un nuevo valor al diccionario del elemento actual con formato/valor: "Children"= X que dirá cuantos elemntos hay dentro
				tree[lvl]["folders"][-1]["children"]=elem["folder"]["childCount"]
				subcarpetas[lvl].append(elem["id"])
		
		# Si hay un fichero en el nivel,
		if "file" in elem:
			# Y aún no existe el diccionario files, lo crea y añade a la lista el elemento actual.
			if "files" not in tree[lvl]:
				tree[lvl]["files"]=[]
				tree[lvl]["files"].append(dict(name=elem["name"],parent=elem["parentReference"]["path"],id=elem["id"],download=elem["@microsoft.graph.downloadUrl"],type=elem["file"]["mimeType"]))
			# si existe añade a la lista de files un nuevo diccionario con el nombre del fichero.
			else:
				tree[lvl]["files"].append(dict(name=elem["name"],parent=elem["parentReference"]["path"],id=elem["id"],download=elem["@microsoft.graph.downloadUrl"],type=elem["file"]["mimeType"]))
	return tree,subcarpetas

def ObtenerNivel(path):
	# Devuelve el nivel en el que está el elemento.
	# Si el path del padre es root devueve nivel 0.
	if len(path.split("/drive/root:/")) == 1:
		return 0
	else:
		return len(path.split("/drive/root:/")[1].split("/"))

def AjustarUnidad(v_bytes):
	if v_bytes >= 1024**4:
		unidad=" TB"
		v_bytes=str(round(v_bytes/1024**4,2))+unidad
	elif v_bytes >= 1024**3:
		unidad=" GB"
		v_bytes=str(round(v_bytes/1024**3,2))+unidad
	elif v_bytes >= 1024**2:
		unidad=" MB"
		v_bytes=str(round(v_bytes/1024**2,2))+unidad
	elif v_bytes >= 1024:
		unidad=" KB"
		v_bytes=str(round(v_bytes/1024,2))+unidad
	else:
		unidad=" bytes"
		v_bytes=v_bytes+unidad
	return v_bytes