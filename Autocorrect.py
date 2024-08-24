import re

def corregir(ubicacion):
    
    ubicacion_buscada = ubicacion.lower()
    #Diccionario de Patrones que deben cumplir las entradas para ser corregidas por una o por otra
    patrones = {
        'Aguascalientes': re.compile(r'(?=.*a)(?=.*g)(?=.*e)(?=.*s)(?=.*l)(?=.*n)'),
        'Amsterdam': re.compile(r'(?=.*a)(?=.*m)(?=.*t)(?=.*d)(?=.*s)'),
        'Arizona': re.compile(r'(?=.*a)(?=.*z)(?=.*r)(?=.*n)'),
        'Atlanta': re.compile(r'(?=.*a)(?=.*t)(?=.*n)(?=.*l)'),
        'Baja California': re.compile(r'(?=.*b)(?=.*\s)(?=.*j){3}(?=.*a)(?=.*c)(?=.*l)'),
        'Belice': re.compile(r'(?=.*b)(?=.*e)(?=.*c)(?=.*i)'),
        'Bogota': re.compile(r'(?=.*b)(?=.*o)(?=.*g)(?=.*t)'),
        'California': re.compile(r'(?=.*c)(?=.*l)(?=.*f)(?=.*a)(?=.*r)(?=.*i)'),        
        'Callao': re.compile(r'(?=.*c){2}(?=.*l)(?=.*a)'),
        'Campeche': re.compile(r'(?=.*c)(?=.*p)(?=.*h)(?=.*m)'),
        'Charlotte': re.compile(r'(?=.*c){2}(?=.*t)(?=.*h)(?=.*r)(?=.*l)'),
        'Chicago': re.compile(r'(?=.*c)(?=.*g)(?=.*h)'),
        'Chihuahua': re.compile(r'(?=.*c){2}(?=.*h){2}(?=.*a)'),
        'Ciudad de Mexico': re.compile(r'(?=.*c)(?=.* )(?=.*d)(?=.*i)(?=.*m)(?=.*x)'),
        'Coahuila': re.compile(r'(?=.*c)(?=.*l)(?=.*a)(?=.*o)'),
        'Florida': re.compile(r'(?=.*f)(?=.*l)(?=.*r)(?=.*d)'),
        'Guerrero': re.compile(r'(?=.*g)(?=.*e){2}(?=.*r)'),
        'Guanajuato': re.compile(r'(?=.*g)(?=.*j){2}(?=.*a)(?=.*t)(?=.*n)'),
        'Guatemala': re.compile(r'(?=.*g)(?=.*t)(?=.*a)(?=.*l)(?=.*m)'),
        'Habana': re.compile(r'(?=.*h)(?=.*b){2}(?=.*a)(?=.*n)'),
        'Houston': re.compile(r'(?=.*h)(?=.*o)(?=.*t)(?=.*n)(?=.*s)'),
        'Jalisco': re.compile(r'(?=.*j)(?=.*l)(?=.*s)(?=.*c)'),
        'Madrid': re.compile(r'(?=.*m)(?=.*d)(?=.*r)'),
        'Monterrey': re.compile(r'(?=.*m)(?=.*r)(?=.*t)(?=.*y)'),
        'Nueva York': re.compile(r'(?=.*n)(?=.* )(?=.v*)(?=.*r)(?=.*y)(?=.*k)'),
        'Oaxaca': re.compile(r'(?=.*o)(?=.*a)(?=.x*)(?=.*c)'),
        'Padahuel': re.compile(r'(?=.*p)(?=.*d)(?=.a*)(?=.*h)(?=.*l)'),
        'Paris': re.compile(r'(?=.*p)(?=.*r)(?=.s*)'),
        'Philadelphia': re.compile(r'(?=.*p)(?=.*h){2}(?=.l*)(?=.*a)(?=.*i)'),
        'Puebla': re.compile(r'(?=.*p)(?=.*b)(?=.l*)'),
        'Queretaro': re.compile(r'(?=.*q)(?=.*e){2}(?=.r*)(?=.*t)'),
        'Quintana Roo': re.compile(r'(?=.*q)(?=.*a){2}(?=.n*)(?=.*t)(?=.r*)(?=.*o)(?=.* )'),
        'San Luis Potosi': re.compile(r'(?=.*s)(?=.*n){2}(?=. *)(?=.*l)(?=.s*)(?=.*p)(?=.t*)(?=.*o)'),
        'Sinaloa': re.compile(r'(?=.*s)(?=.*n)(?=.a*)(?=.*l)'),
        'Sonora': re.compile(r'(?=.*s)(?=.*r)(?=.*o)(?=.*n)'),
        'Tabasco': re.compile(r'(?=.*t)(?=.*a)(?=.*b)(?=.*s)(?=.*c)'),
        'Tamaulipas': re.compile(r'(?=.*t){2}(?=.*a)(?=.*m)(?=.*s)(?=.*p)(?=.*l)'),
        'Texas': re.compile(r'(?=.*t)(?=.*x)(?=.*s)'),       
        'Toluca': re.compile(r'(?=.*t)(?=.*l)(?=.*c)'),
        'Toronto': re.compile(r'(?=.*t){2}(?=.*o)(?=.*r)(?=.*n)'),
        'Vancouver': re.compile(r'(?=.*v)(?=.*n)(?=.*c)(?=.*r)(?=.*e)'),
        'Veracruz': re.compile(r'(?=.*v){2}(?=.*r)(?=.*c)(?=.*z)'),
        'Yucatan': re.compile(r'(?=.*y)(?=.*a)(?=.*c)(?=.*t)(?=.*n)'),
        'Zacatecas': re.compile(r'(?=.*z){2}(?=.*a){2}(?=.*c)(?=.*t)(?=.*s)'),
    }
    # Verificar si la ubicación buscada coincide con algún patrón y de ser asi se devuelve la correccion
    for ciudad, patron in patrones.items():
        if ubicacion_buscada.startswith(ciudad[0].lower()) and patron.search(ubicacion_buscada):
            return ciudad
    
    return None