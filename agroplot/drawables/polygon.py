from agroplot.color import _get_hex_color
from agroplot.utility import _format_LatLng
from random import random

class _Polygon(object):
    def __init__(self, lats, lngs, precision, **kwargs):
        '''
        Args:, 
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

        self._info = kwargs.get('info')
        self._objectid = 'polygon_' + str(int(10e6 * random()))



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
        if self._info is not None:
            if self._info.get('descripcion') is not None: h = h + "<h3>" + self._info.get('descripcion') + "</h3>"
            rect_tipo = "<svg width='10' height='9'><rect width='8' height='8' style='fill:" + self._info.get('tipo_color') + ";stroke-width:0;fill-opacity:0.85;'/></svg> "
            if self._info.get('tipo') is not None: h = h + rect_tipo + " <b>Cultivo: </b>" + self._info.get('tipo')
            if (self._info.get('variedad') is not None) and (self._info.get('variedad') != self._info.get('tipo')): h = h + " / " + self._info.get('variedad')
            rect_propietario = "<svg width='10' height='9'><rect width='8' height='8' style='fill:" + self._info.get('propietario_color') + ";stroke-width:0;fill-opacity:0.85;'/></svg> "
            if self._info.get('propietario') is not None: h = h + "<br>" + rect_propietario + " <b>Propietario: </b>" + self._info.get('propietario')
            rect_dummy = "<svg width='10' height='9'><rect width='8' height='8' style='fill:white;stroke-width:0;fill-opacity:0;'/></svg> "
            if self._info.get('municipio') is not None: h = h+ "<br>" + rect_dummy + " <b>Referencia: </b>" + self._info.get('municipio')
            if self._info.get('poligono') is not None: h = h + " / " + self._info.get('poligono')
            if self._info.get('parcela') is not None: h = h + " / " + self._info.get('parcela')
            if (self._info.get('recinto') is not None) and (self._info.get('recinto') != '0'): h = h + " / " +  self._info.get('recinto')
            if self._info.get('extension') is not None: h = h + "<br>" + rect_dummy + " <b>Extensión: </b>" + self._info.get('extension')

        return h

