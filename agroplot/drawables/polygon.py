from agroplot.color import _get_hex_color
from agroplot.utility import _format_LatLng
from random import random

class _Polygon(object):
    def __init__(self, lats, lngs, precision, info, **kwargs):
        '''
        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            edge_color (str): Color of the polygon's edge. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            edge_alpha (float): Opacity of the polygon's edge, ranging from 0 to 1.
            edge_width (int): Width of the polygon's edge, in pixels.
            face_color (str): Color of the polygon's face. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            face_alpha (float): Opacity of the polygon's face, ranging from 0 to 1.
        '''
        self._points = [_format_LatLng(lat, lng, precision) for lat, lng in zip(lats, lngs)]
                
        edge_color = kwargs.get('edge_color')
        self._edge_color = _get_hex_color(edge_color) if edge_color is not None else None

        self._edge_alpha = kwargs.get('edge_alpha')
        self._edge_width = kwargs.get('edge_width')

        face_color = kwargs.get('face_color')
        self._face_color = _get_hex_color(face_color) if face_color is not None else None

        self._face_alpha = kwargs.get('face_alpha')
        
        self._objectid = 'polygon_' + str(int(10e6 * random()))
        self._text_descripcion = info.get('descripcion', None)
        self._text_tipo = info.get('tipo', None)
        self._text_variedad = info.get('variedad', None)
        self._text_municipio = info.get('municipio', None)
        self._text_poligono = info.get('poligono', None)
        self._text_parcela = info.get('parcela', None)
        self._text_recinto = info.get('recinto', None)
        self._text_propietario = info.get('propietario', None)
        self._text_extension = info.get('extension', None)


    def write(self, w):
        '''
        Write the polygon.

        Args:
            w (_Writer): Writer used to write the polygon.
        '''
        w.write('%s = new google.maps.Polygon({' % self._objectid)
        w.indent()
        w.write('clickable: true,')
        w.write('geodesic: true,')
        if self._edge_color is not None: w.write('strokeColor: "%s",' % self._edge_color)
        if self._edge_alpha is not None: w.write('strokeOpacity: %f,' % self._edge_alpha)
        if self._edge_width is not None: w.write('strokeWeight: %d,' % self._edge_width)
        if self._face_color is not None: w.write('fillColor: "%s",' % self._face_color)
        if self._face_alpha is not None: w.write('fillOpacity: %f,' % self._face_alpha)
        w.write('map: map,')
        w.write('paths: [')
        w.indent()
        [w.write('%s,' % point) for point in self._points]
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        
        s_texto = '' 
        if self._text_descripcion is not None: s_texto = s_texto + self._text_descripcion
        if self._text_tipo is not None: s_texto = s_texto + '\\n - Tipo: ' + self._text_tipo
        if (self._text_variedad is not None) and (self._text_variedad != self._text_tipo): s_texto = s_texto + '\\n - Variedad: ' + self._text_variedad
        if self._text_propietario is not None: s_texto = s_texto + '\\n - Propietario: ' + self._text_propietario
        if self._text_municipio is not None: s_texto = s_texto + '\\n - Municipio: ' + self._text_municipio
        if self._text_poligono is not None: s_texto = s_texto + '\\n - Polígono: ' + self._text_poligono
        if self._text_parcela is not None: s_texto = s_texto + '\\n - Parcela: ' + self._text_parcela
        if (self._text_recinto is not None) and (self._text_recinto != '0'): s_texto = s_texto + '\\n - Recinto: ' + self._text_recinto
        if self._text_extension is not None: s_texto = s_texto + '\\n - Extensión: ' + self._text_extension

        w.write("google.maps.event.addListener(%s, 'click', function (e) {" % self._objectid)
        w.indent()
        w.write('alert("' + s_texto + '")')
        w.dedent()
        w.write('});')

        w.write()
