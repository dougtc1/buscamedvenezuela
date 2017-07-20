from django.http import HttpResponse
from django.template import loader
from .models import Activo, Medicina, Presentacion, Tweet
import urllib.request, json
from django.contrib import messages
from django.shortcuts import redirect

# Usar esta lista para ignorar esas medicinas al buscar en el streamming (ayudan a reducir cantidad de tweets encontrados)

quitarComunes = ["CALCIO","ARANDA","OTAN","HIERRO","DUPLA","BICARBONATO","DIP",
					"FRICCION","CLORURO","REFRESH","EVRA","COST","FLUIR","MAILEN",
					"ADRENALINA","VICK","ALLER","VIAGRA","NOVA","VITAMINA C","ACTOS",
					"ZAP","NAS","KALI","CASTE","DOL","SAVER","SAGAL","RECITA","QUIN",
					"VENTUS", "TEMPRA", "SAX","VITAE","GABOX","ENAM","SELENE","SELES",
					"TARON", "CAMPAL","AZA","YAZ","KIR","CIFRAN","MIRENA","ENO","CLARIX",
					"PINAZO","ARNOL"]

# Boton del "home", te lleva a la pagina principal
def goHome(request):
	template = loader.get_template('app/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def lista(request):
	template = loader.get_template('app/lista.html')
	activo_list = Activo.objects.order_by('componente')
	context = {
		'activo_list': activo_list,
	}
	return HttpResponse(template.render(context, request))

# Pagina principal, antes mostraba todos los componentes activos en la pagina principal
def index(request):
	template = loader.get_template('app/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

# Función que verifica que la medicina buscada por el usuario se encuentra en la base de datos
def searchDataBase(request):
	raw_search_query = request.GET.get('search_box', None)
	search_query = raw_search_query.upper()
	
	if search_query:
		# Se busca primero la medicina (es lo mas probable que se busque de primero)
		try:
			medicina = Medicina.objects.filter(nombre=search_query)
			if medicina:
				if type(medicina) is not Medicina:
					medicina = medicina[0]
			activo = Activo.objects.get(componente=medicina.activo)
			medicina = Medicina.objects.filter(activo=activo).order_by('nombre')
		except:
			try:
				activo = Activo.objects.get(componente=search_query)
				medicina = Medicina.objects.filter(activo=activo).order_by('nombre')
			except:
				messages.add_message(request, messages.ERROR, 'Disculpe, \'' + raw_search_query +'\' no es reconocido en nuestra base de datos.')
				template = loader.get_template('app/index.html')				
				context = {'messages':messages}
				return (None,redirect('/app',context),True)
		return (activo,medicina,False)
	
	else:
		messages.add_message(request, messages.ERROR, 'Disculpe, no puede dejar este campo vacío.')
		template = loader.get_template('app/index.html')				
		context = {'messages':messages}
		return (None,redirect('/app',context),True)
		

# Funcion que dada cierta medicina, la busca en la bd y se le presenta al usuario esta y demas medicinas equivalentes
def searchFamily(request):
	# Se agregó lo de problema para casos en los que la persona escribia una medicina que no existia
	activo,medicina,problema = searchDataBase(request)
	if problema:
		return medicina
	presentacion = []
	if type(medicina) is Medicina:
		presentacion.append(Presentacion.objects.filter(medicina=medicina))
	else:
		for i in medicina:
			presentacion.append(Presentacion.objects.filter(medicina=i))
	template = loader.get_template('app/search.html')
	context = {
	'activo': activo.componente,
	'medicina': medicina,
	'presentacion': presentacion,
	'busqueda':	request.GET.get('search_box', None)
	}
	return HttpResponse(template.render(context, request))

# Aqui se hace lo de la busqueda de los tweets en la base de datos y antes, la llamada al api para hacer streamming
def retrieveTweets(listaMedicinas,tipo):
	listaTweets = []	
	for i in listaMedicinas:
		tweets = Tweet.objects.filter(medicina=i,clasificacion=tipo)
		for j in tweets:
			listaTweets.append(j.link)
	# Ya tengo los tweets, ahora debo mostrarlos en la pagina
	return listaTweets
			
# Funcion que se encarga de la busqueda de los tweets, tanto de oferta como de demanda
def buscaTweets(request):
	if request.META["PATH_INFO"] == "/app/tweetsOferta/":
		tipoBusqueda = "oferta"
	elif request.META["PATH_INFO"] == "/app/tweetsDemanda/":
		tipoBusqueda = "demanda"
	else:
		return error(request)
	# Se agregó lo de problema para casos en los que la persona escribia una medicina que no existia
	activo,listaMedicinas,problema = searchDataBase(request)
	if problema:
		return listaMedicinas
	# Se quitan aquellas medicinas con que son palabras comunes y que tienen otras medicinas "mas representativas"
	for i in quitarComunes:
		if i in listaMedicinas:
			listaMedicinas.remove(i)
			break
	listaTweets = retrieveTweets(listaMedicinas,tipoBusqueda)
	# Se hace la obtencion del codigo html de la api de Twitter para mostrarlos en la pagina
	embed = "https://publish.twitter.com/oembed?url="
	listaHtml = []
	for link in listaTweets:
		url = urllib.request.urlopen(embed + link)
		response = json.loads(url.read().decode())
		listaHtml.append(response['html'])

	if len(listaHtml) == 0:
		vacio = True
	else:
		vacio = False
	template = loader.get_template('app/tweets.html')
	aux = []
	for i in listaMedicinas:
		aux.append(i.nombre)
	setMedicinas = set(aux)
	context = {'listaHtml' : listaHtml,
				'busqueda' : request.GET.get('search_box', None),
				'vacio' : vacio,
				'setMedicinas' : setMedicinas,
				'tipoBusqueda' : tipoBusqueda}
	return HttpResponse(template.render(context, request))
