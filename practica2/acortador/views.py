from django.shortcuts import render
from django.http import HttpResponse
from models import URL
from django.views.decorators.csrf import csrf_exempt
import urllib
# Create your views here.

@csrf_exempt
def url(request, url):
			
	if request.method == 'GET':
		if url == '':
			respuesta = '<form method="POST" action="">' \
				+ 'URL: <input type="text" name="url"><br>' \
				+ '<input type="submit" value="Enviar"><br>' \
				+ '</form>' 
			paginas = URL.objects.all()
			for pagina in paginas:
				respuesta += '<li><a href="/' + str(pagina.URLcorta) + '">' + str(pagina.URLlarga) + '</a>'
				respuesta += '<li><a href="/' + str(pagina.URLcorta) + '">' + str(pagina.URLcorta) + '</a>'
			
		else:

			try:
				pagina = URL.objects.get(URLcorta=url)
				respuesta = '<html><head><meta http-equiv="Refresh" content="5;url='+ pagina.URLlarga +'"></head>' \
				+ "<body><h1> Espere, va a ser redirigido en 5 segundos... " \
				+ "</h1></body></html>"
			except URL.DoesNotExist:
				try:
					url = 'http://localhost:1234/' + str(url)
					pagina = URL.objects.get(URLcorta=url)
					respuesta = '<html><head><meta http-equiv="Refresh" content="5;url='+ pagina.URLlarga +'"></head>' \
						+ "<body><h1> Espere, va a ser redirigido en 5 segundos... " \
						+ "</h1></body></html>"
				except URL.DoesNotExist:
					respuesta = '<h1><font color ="red">Lo sentimos esta pagina no ha sido almacenada.</font></h1>'
		return HttpResponse(respuesta)
	
	elif request.method == 'POST' or request.method == 'PUT':
		urlparaacortar = request.body.split("=")[1]
		urlparaacortar = urllib.unquote(urlparaacortar).decode('utf8')
		http = urlparaacortar.split("://")[0]

		if (http != 'http') and (http != 'https'):
			urlparaacortar = 'https://' + str(urlparaacortar)
		
		try:
			urlcorta = URL.objects.get(URLlarga=urlparaacortar)
			respuesta = '<h1>Esta URL ya ha sido acortada </h1></br>'\
				+'<html><body><a href="'+ urlparaacortar +'">' + urlparaacortar + ' </a></br></body></html>'\
				+ '<html><body><a href="'+ urlcorta.URLcorta +'">'+ urlcorta.URLcorta + ' </a></br></body></html>' 
		
		except URL.DoesNotExist:
			paginas = URL.objects.all()
			contador = 0
			for pagina in paginas:
				contador = contador + 1
			urlnuevacorta = 'http://localhost:1234/' + str(contador)
			p = URL(URLcorta=urlnuevacorta, URLlarga=urlparaacortar)
			p.save()
			pagina = URL.objects.get(URLcorta=urlnuevacorta)
			respuesta = "<h1>Se ha acortado la URL de forma correcta</br></h1>" \
				+'<a href="'+ str(pagina.URLlarga) +'">' + str(pagina.URLlarga) + ' </a></br>'\
				+ '<a href="'+ str(pagina.URLcorta) +'">'+ str(pagina.URLcorta) + ' </a></br>'

		return HttpResponse(respuesta)

	else:
		respuesta= 'Ha ocurrido un error'
		return HttpResponse(respuesta)



		
	
