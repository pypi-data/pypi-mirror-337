
from ..constants import *
from ..utils import *
import gdsfactory as gf
from gdsfactory.cross_section import Section
from networkx import center
from numpy import cumsum
from gdsfactory.generic_tech import LAYER_STACK, LAYER

# import .utils as utils
# from layers import *


def port_bbox(p):
    c = np.array(p.center)
    v = p.width/2*np.array([np.sin(np.radians(p.orientation)),
                           -np.cos(np.radians(p.orientation))])
    return [(c-v).tolist(), (c+v).tolist()]


def mimo(west=0, east=0, south=0, north=0,
         in_ports=[], out_ports=[],
         l=2.0, w=2.0, wwg=.5, lwg=None, taper=0.06,
         wwg_west=None, wwg_east=None, wwg_south=None, wwg_north=None,
         wwg_layer=LAYER.WG,  # BBOX=LAYER.WAFER,
         CANVAS_LAYER=CANVAS_LAYER,
         **kwargs):
    design = gf.Component()
    c = gf.Component(**kwargs)
    if lwg is None:
        lwg = 5*wwg
    p = [(0, 0), (l, 0), (l, w), (0, w)]
    design.add_polygon(p,                       layer=CANVAS_LAYER)
    if not in_ports:
        c.add_polygon(p,                       layer=wwg_layer)

    ld = [west,  east, south, north]
    for i, v, d in zip(range(4), ld, [w, w, l, l]):
        if type(v) is int:
            ld[i] = [(.5+j)*d/v for j in range(v)]
    lwwg = [wwg_west, wwg_east, wwg_south, wwg_north]
    for i, v in enumerate(lwwg):
        if v is None:
            v = wwg
        if type(v) is float or type(v) is int:
            lwwg[i] = [v]*len(ld[i])

    n = 0
    for (i, x, y, d, wwg, a) in zip(
        range(4),
        [0,  l, 0, 0],
        [0, 0, 0, w],
        ld,
        lwwg,
        [180, 0, -90, 90]
    ):
        for wwg, v in zip(wwg, d):
            center = (x, y+v) if i in [0, 1] else (x+v, y)
            wwg2 = wwg+taper*lwg
            name = "o"+str(n+1)
            design.add_port(name, center=center, width=wwg2,
                            orientation=a, layer=wwg_layer)
            wg = c << gf.components.taper(
                length=lwg, width1=wwg, width2=wwg2, layer=wwg_layer)
            wg.connect("o2", design.ports[name])
            c.add_port(name, port=wg.ports["o1"])
            n += 1

    design = c << design
    for i in in_ports:
        for j in out_ports:
            pi = design.ports[f'o{i}']
            pj = design.ports[f'o{j}']
            # a = port_bbox(design.ports[f'o{i}'])
            # b = port_bbox(design.ports[f'o{j}'])
            p1 = np.array(pi.center)
            p2 = np.array(pj.center)
            n1 = np.array([cos(np.radians(pi.orientation)),
                           sin(np.radians(pi.orientation))])
            n2 = np.array([cos(np.radians(pj.orientation)),
                           sin(np.radians(pj.orientation))])
            v = p2-p1
            d = np.linalg.norm(v)
            v = v/d
            l = [p1,
                 p1-.4*d*n1,
                 #  p1+.5*d*(.3*v-.7*n1),
                 #  p2+.5*d*(-.3*v-.7*n2),
                 p2-.4*d*n2,
                 p2]
            c << gf.components.bends.bezier(
                [x.tolist() for x in l],
                # start_angle=pi.orientation-180,
                # end_angle=pj.orientation,
                allow_min_radius_violation=True,
                width=pi.width,)  # layer=wwg_layer)
            # c.add_polygon(a+b, layer=wwg_layer)
    return c
