from agroplot.utility import _format_LatLng
from agroplot.drawables.marker_icon import _MarkerIcon
from agroplot.drawables.marker_info_window import _MarkerInfoWindow
from agroplot.drawables.raw_marker import _RawMarker

class _Marker(object):
    def __init__(self, lat, lng, color, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the marker.
            lng (float): Longitude of the marker.
            color (str): Marker color. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            title (str): Hover-over title of the marker.
            label (str): Label displayed on the marker.
            info_window (str): HTML content to be displayed in a pop-up `info window`_.
            draggable (bool): Whether or not the marker is `draggable`_.

        .. _info window: https://developers.google.com/maps/documentation/javascript/infowindows
        .. _draggable: https://developers.google.com/maps/documentation/javascript/markers#draggable
        '''
        self._marker_icon = _MarkerIcon(color)

        #info_window = kwargs.pop('info_window', None)
        #self._marker_info_window = _MarkerInfoWindow(info_window) if info_window is not None else None
        self._info = kwargs.get('info')
        info_html = self._make_label()
        self._marker_info_window = _MarkerInfoWindow(info_html) if info_html != '' else None

        self._raw_marker = _RawMarker(
            _format_LatLng(lat, lng, precision),
            self._marker_icon.get_name(),
            **kwargs
        )



    def write(self, w, context):
        '''
        Write the marker.

        Args:
            w (_Writer): Writer used to write the marker.
            context (_Context): Context used to keep track of what was drawn to the map.
        '''
        # Write the marker icon (if it isn't written already):
        self._marker_icon.write(w, context)

        # If this marker has no associated info window, just write the marker as is:
        if self._marker_info_window is None:
            self._raw_marker.write(w)

        # Otherwise, write the marker with its info window:
        else:
            marker_name = ('info_marker_%d' % context.num_info_markers)
            self._raw_marker.write(w, marker_name)
            self._marker_info_window.write(w, context, marker_name)
            context.num_info_markers += 1


    def _make_label(self):
        h = ""
        if self._info is not None:
            if self._info.get('descripcion') is not None: h = h + "<h3>" + self._info.get('descripcion') + "</h3>"
            rect_html = "<svg width='10' height='9'><rect width='8' height='8' style='fill:" + self._info.get('tipo_color') + ";stroke-width:0;fill-opacity:0.85;'/></svg> "
            if self._info.get('tipo') is not None: h = h + rect_html + " <b>Tipo: </b>" + self._info.get('tipo')

        return h
