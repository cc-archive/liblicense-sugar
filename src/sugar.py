# Creative Commons has made the contents of this file
# available under a CC-GNU-LGPL license:
#
# http://creativecommons.org/licenses/LGPL/2.1/
#
# A copy of the full license can be found as part of this
# distribution in the file COPYING.
# 
# You may use the liblicense software in accordance with the
# terms of that license. You agree that you are solely 
# responsible for your use of the liblicense software and you
# represent and warrant to Creative Commons that your use
# of the liblicense software will comply with the CC-GNU-LGPL.
#
# Copyright 2007, Creative Commons, www.creativecommons.org.
# Copyright 2007, Scott Shawcroft.

import liblicense as ll
import gtk
import hippo

from sugar.graphics.icon import Icon
from sugar.graphics.xocolor import XoColor
from sugar.graphics.canvasicon import CanvasIcon
from sugar.graphics.palette import Palette

class LicenseWidget:
    """ Provides generic license widget funcitonalities.
    """
    ICON_SCALE = 2
    
    _licenses = (("http://creativecommons.org/licenses/by/3.0/","cc-by"),
                ("http://creativecommons.org/licenses/by-sa/3.0/","cc-by-sa"),
                ("http://creativecommons.org/licenses/by-nd/3.0/","cc-by-nd"),
                ("http://creativecommons.org/licenses/by-nc/3.0/","cc-by-nc"),
                ("http://creativecommons.org/licenses/by-nc-sa/3.0/","cc-by-nc-sa"),
                ("http://creativecommons.org/licenses/by-nc-nd/3.0/","cc-by-nc-nd"))
                
    def __init__(self,jobject,default_colors="#000000,#000000"):
        self._jobject = jobject
        self._default_colors = default_colors
        self.register_icon_size()
    
    def load_license(self):
        license = ll.read(self._jobject.get_file_path())
        default = False
        if not license:
            license = ll.get_default()
            default=True
        return (default,license)
    
    def get_icon(self,license):
        if license and license in map(lambda x: x[0],self._licenses):
            current_icon = "cc-" + license.split("/")[4]
        else:
            current_icon = "cc-by"
        return current_icon
    
    def get_icon_color(self,default):
        if default:
            color = XoColor(self._default_colors)
        else:
            color = XoColor(self._jobject.metadata['icon-color'])
        return color
    
    def _license_cb(self,widget,uri):
        print self._jobject.get_file_path(),license
        print ll.write(self._jobject.get_file_path(),license)

    def make_menu(self,palette,color,color_selected,current_icon):
        for uri, icon_name in self._licenses:
            tmp = gtk.HBox()
            tmp.show()
            icon = Icon(icon_name,self._icon_size)
            if current_icon==icon_name:
                icon.props.xo_color = color_selected
            else:
                icon.props.xo_color = color
            
            icon.show()
            tmp.pack_start(icon,False,False)
            item = gtk.MenuItem()
            item.add(tmp)
            item.connect('activate', self._license_cb,uri)
            palette.menu.append(item)
            item.show()
    
    def register_icon_size(self):
        self._icon_size = gtk.icon_size_from_name("license-icon-size")
        if self._icon_size==0:
            self._icon_size = gtk.icon_size_register("license-icon-size", int(76*self.ICON_SCALE), int(21*self.ICON_SCALE))
        return self._icon_size
        

class CanvasLicense(LicenseWidget,CanvasIcon):
    def __init__(self,jobject,menu=True):
        LicenseWidget.__init__(self,jobject)
        default, license = self.load_license()
        color = self.get_icon_color(default)
        icon_name = self.get_icon(license)
        
        CanvasIcon.__init__(self,icon_name="theme:"+icon_name,
                                xalign=hippo.ALIGNMENT_END,
                                scale=self.ICON_SCALE)

        self.props.xo_color = color
        self.set_tooltip(ll.get_name(license))
        
        if menu:
            palette = self.get_palette()
            self.make_menu(palette,XoColor("#ffffff,#ffffff"),XoColor(self._jobject.metadata['icon-color']),icon_name)
            palette.props.position = Palette.BOTTOM
