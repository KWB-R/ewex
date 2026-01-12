import dataclasses as dtc


@dtc.dataclass
class Matrix:
    id: str
    name: str
    description: str

    def __repr__(self):
        return f"Matrix({self.id}, {self.name})"


class Matrices:
    iww = Matrix("iww", "Industrial wastewater", "Raw wastewater from industrial sources")
    hww = Matrix("hww", "Household wastewater", "Raw wastewater from households")
    lww = Matrix("lww", "Landfill leachate", "Landfill leachate")
    rww = Matrix("rww", "Raw wastewater", "Raw wastewater from various sources (dominated by houshold wastewater)")
    tiw = Matrix("tiw", "Treated industrial wastewater",
                 "Industrial or landfill leachate after wastewater treatment (not further specified, only used for site specific data)")
    tww = Matrix("tww", "Treated wastewater", "Wastewater after primary and secondary treatment")
    stw = Matrix("stw", "Stormwater runoff", "Urban stormwater runoff")
    raw = Matrix("raw", "Rainwater", "Rainwater without runoff")
    suw = Matrix("suw", "Surface water", "Surfacewater")
    grw = Matrix("grw", "Groundwater", "Groundwater")
    pow = Matrix("pow", "Soil pore water", "Soil leachate")
    bfw = Matrix("bfw", "Bank filtrate", "Bank filtrate")
    drw = Matrix("drw", "Drinking water", "Drinking water after treatment")
    sdg = Matrix("sdg", "Sludge",
                 "Thickened sludge from treated wastewater (as part of the secondary wastewater treatment)")
    no_change = None
