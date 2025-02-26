from agroplot.color import _get_hex_color
from agroplot.utility import _format_LatLng
from random import random

class _Circle(object):
    def __init__(self, lat, lng, radius, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the circle.
            lng (float): Longitude of the center of the circle.
            radius (int): Radius of the circle, in meters.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            edge_color (str): Color of the circle's edge. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            edge_alpha (float): Opacity of the circle's edge, ranging from 0 to 1.
            edge_width (int): Width of the circle's edge, in pixels.
            face_color (str): Color of the circle's face. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            face_alpha (float): Opacity of the circle's face, ranging from 0 to 1.
        '''
        self._center = _format_LatLng(lat, lng, precision)
        self._radius = radius

        edge_color = kwargs.get('edge_color')
        self._edge_color = _get_hex_color(edge_color) if edge_color is not None else None

        self._edge_alpha = kwargs.get('edge_alpha')
        self._edge_width = kwargs.get('edge_width')

        face_color = kwargs.get('face_color')
        self._face_color = _get_hex_color(face_color) if face_color is not None else None

        self._face_alpha = kwargs.get('face_alpha')
        
        self._info = kwargs.get('info')
        self._objectid = 'circle_' + str(int(10e6 * random()))



    def write(self, w):
        '''
        Write the circle.

        Args:
            w (_Writer): Writer used to write the circle.
        '''
        w.write('%s = new google.maps.Circle({' % self._objectid)
        w.indent()
        w.write('clickable: true,')
        w.write('geodesic: true,')
        if self._edge_color is not None: w.write('strokeColor: "%s",' % self._edge_color)
        if self._edge_alpha is not None: w.write('strokeOpacity: %s,' % self._edge_alpha)
        if self._edge_width is not None: w.write('strokeWeight: %s,' % self._edge_width)
        if self._face_color is not None: w.write('fillColor: "%s",' % self._face_color)
        if self._face_alpha is not None: w.write('fillOpacity: %s,' % self._face_alpha)
        w.write('center: %s,' % self._center)
        w.write('radius: %s,' % self._radius)
        w.write('map: map')
        w.dedent()
        w.write('});')

        etiqueta = self._make_label()
        if etiqueta != '':
            w.write('google.maps.event.addListener(' + self._objectid + ', "click", function(event) { ')
            w.indent()
            w.write('infowindow.setContent("' + etiqueta + '"); ')
            w.write('infowindow.setPosition(event.latLng); ')
            w.write('infowindow.open(map, ' + self._objectid + '); ')
            w.dedent()
            w.write('});')

        w.write()


    def _make_label(self):
        h = ""
        if (self._info is not None) & (self._info.get('descripcion') is not None) & (self._info.get('descripcion') != ''):
            if self._info.get('descripcion') is not None: h = h + "<h3>" + self._info.get('descripcion') + "</h3>"
            if self._info.get('tipo_color') == 'white': 
                s_stroke = '#A0A0A0' 
            else: 
                s_stroke = self._info.get('tipo_color')
            rect_tipo = "<svg width='10' height='9'><rect width='8' height='8' style='fill:" + self._info.get('tipo_color') + ";stroke-width:1;stroke:" + s_stroke + ";fill-opacity:0.85;'/></svg> "
            if self._info.get('propietario_color') == 'white': 
                s_stroke_prop = '#A0A0A0' 
            else: 
                s_stroke_prop = self._info.get('propietario_color')
            if (self._info.get('tipo') is not None) & (self._info.get('tipo') != ''): h = h + rect_tipo + " <b>Tipo: </b>" + self._info.get('tipo') +"<br>"
            rect_propietario = "<svg width='10' height='9'><rect width='8' height='8' style='fill:" + self._info.get('propietario_color') + ";stroke-width:1;stroke:" + s_stroke_prop + ";fill-opacity:0.85;'/></svg> "
            if (self._info.get('propietario') is not None) & (self._info.get('propietario') != ''): h = h + rect_propietario + " <b>Propietario: </b>" + self._info.get('propietario')
        else:
            h = h + "<h3>Punto de interés</h3>"

        return h

