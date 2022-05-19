import spot, buddy
from spot.aux_ import str_to_svg

_dummy_g = spot.make_twa_graph()

def make_ap(name:"str")->"buddy.bdd":
    return buddy.bdd_ithvar(_dummy_g.register_ap(name))

def show_bdd(abdd:"buddy.bdd")->"svg":
    from spot.jupyter import SVG
    buddy.bdd_fnprintdot(".bdddump.dot", abdd)
    with open(".bdddump.dot", "r") as fdump:
        s = "".join(fdump.readlines())
        return SVG(str_to_svg(s.encode('utf-8')))