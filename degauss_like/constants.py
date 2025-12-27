# coding: utf-8
"""Constants module for US address parsing.

This module provides bidirectional mappings for address components like
street types, directionals, state abbreviations, etc. Based on the Ruby
implementation in degauss-org/geocoder.
"""

import re
from .numbers import Cardinals, Ordinals


class Map(dict):
    """A bidirectional mapping class for address components.
    
    This class extends dict to provide case-insensitive, bidirectional
    mappings between full words and their abbreviations.
    """
    
    def __init__(self, items=None):
        """Initialize the Map.
        
        Args:
            items: Dictionary of items to include in the mapping.
        """
        super().__init__()
        self.regexp = None
        
        if items:
            # Add all items in both directions
            for key, value in items.items():
                super().__setitem__(key, value)
            
            # Build the regex matcher
            self._build_match()
            
            # Add lowercase versions
            keys_list = list(self.keys())
            for k in keys_list:
                super().__setitem__(k.lower(), super().__getitem__(k))
            
            values_list = [v for v in self.values() if isinstance(v, str)]
            for v in values_list:
                if v.lower() not in self:
                    super().__setitem__(v.lower(), v)
    
    def _build_match(self):
        """Build a regular expression to match all keys and values."""
        all_words = []
        for key in list(self.keys()):
            all_words.append(key)
        for value in list(self.values()):
            if isinstance(value, str) and value not in all_words:
                all_words.append(value)
        
        if all_words:
            pattern = r'\b(' + '|'.join(re.escape(w) for w in all_words) + r')\b'
            self.regexp = re.compile(pattern, re.IGNORECASE)
    
    def __getitem__(self, key):
        """Get an item from the mapping (case-insensitive).
        
        Args:
            key: The key to look up.
            
        Returns:
            The value associated with the key.
        """
        if isinstance(key, str):
            key = key.lower()
        return super().__getitem__(key)
    
    def __contains__(self, key):
        """Check if a key exists in the mapping (case-insensitive).
        
        Args:
            key: The key to check.
            
        Returns:
            True if the key exists, False otherwise.
        """
        if isinstance(key, str):
            key = key.lower()
        return super().__contains__(key)
    
    def get(self, key, default=None):
        """Get an item from the mapping with a default value.
        
        Args:
            key: The key to look up.
            default: Default value if key not found.
            
        Returns:
            The value associated with the key or default.
        """
        if isinstance(key, str):
            key = key.lower()
        return super().get(key, default)


# Directional constant maps compass direction words to their abbreviations
Directional = Map({
    "North": "N",
    "South": "S",
    "East": "E",
    "West": "W",
    "Northeast": "NE",
    "Northwest": "NW",
    "Southeast": "SE",
    "Southwest": "SW",
    "Norte": "N",
    "Sur": "S",
    "Este": "E",
    "Oeste": "O",
    "Noreste": "NE",
    "Noroeste": "NO",
    "Sudeste": "SE",
    "Sudoeste": "SO"
})

# Prefix_Qualifier constant maps feature prefix qualifiers to their abbreviations
Prefix_Qualifier = Map({
    "Alternate": "Alt",
    "Business": "Bus",
    "Bypass": "Byp",
    "Extended": "Exd",
    "Historic": "Hst",
    "Loop": "Lp",
    "Old": "Old",
    "Private": "Pvt",
    "Public": "Pub",
    "Spur": "Spr",
})

# Suffix_Qualifier constant maps feature suffix qualifiers to their abbreviations
Suffix_Qualifier = Map({
    "Access": "Acc",
    "Alternate": "Alt",
    "Business": "Bus",
    "Bypass": "Byp",
    "Connector": "Con",
    "Extended": "Exd",
    "Extension": "Exn",
    "Loop": "Lp",
    "Private": "Pvt",
    "Public": "Pub",
    "Scenic": "Scn",
    "Spur": "Spr",
    "Ramp": "Rmp",
    "Underpass": "Unp",
    "Overpass": "Ovp",
})

# Prefix_Canonical constant maps canonical street type prefixes to their abbreviations
Prefix_Canonical = {
    "Arcade": "Arc",
    "Autopista": "Autopista",
    "Avenida": "Ave",
    "Avenue": "Ave",
    "Boulevard": "Blvd",
    "Bulevar": "Bulevar",
    "Bureau of Indian Affairs Highway": "BIA Hwy",
    "Bureau of Indian Affairs Road": "BIA Rd",
    "Bureau of Indian Affairs Route": "BIA Rte",
    "Bureau of Land Management Road": "BLM Rd",
    "Bypass": "Byp",
    "Calle": "Cll",
    "Calleja": "Calleja",
    "Callejón": "Callejón",
    "Caminito": "Cmt",
    "Camino": "Cam",
    "Carretera": "Carr",
    "Cerrada": "Cer",
    "Círculo": "Cír",
    "Commons": "Cmns",
    "Corte": "Corte",
    "County Highway": "Co Hwy",
    "County Lane": "Co Ln",
    "County Road": "Co Rd",
    "County Route": "Co Rte",
    "County State Aid Highway": "Co St Aid Hwy",
    "County Trunk Highway": "Co Trunk Hwy",
    "County Trunk Road": "Co Trunk Rd",
    "Court": "Ct",
    "Delta Road": "Delta Rd",
    "District of Columbia Highway": "DC Hwy",
    "Driveway": "Driveway",
    "Entrada": "Ent",
    "Expreso": "Expreso",
    "Expressway": "Expy",
    "Farm Road": "Farm Rd",
    "Farm-to-Market Road": "FM",
    "Fire Control Road": "Fire Cntrl Rd",
    "Fire District Road": "Fire Dist Rd",
    "Fire Lane": "Fire Ln",
    "Fire Road": "Fire Rd",
    "Fire Route": "Fire Rte",
    "Fire Trail": "Fire Trl",
    "Forest Highway": "Forest Hwy",
    "Forest Road": "Forest Rd",
    "Forest Route": "Forest Rte",
    "Forest Service Road": "FS Rd",
    "Highway": "Hwy",
    "Indian Route": "Indian Rte",
    "Indian Service Route": "Indian Svc Rte",
    "Interstate Highway": "I-",
    "Lane": "Ln",
    "Logging Road": "Logging Rd",
    "Loop": "Loop",
    "National Forest Development Road": "Nat For Dev Rd",
    "Navajo Service Route": "Navajo Svc Rte",
    "Parish Road": "Parish Rd",
    "Pasaje": "Pasaje",
    "Paseo": "Pso",
    "Passage": "Psge",
    "Placita": "Pla",
    "Plaza": "Plz",
    "Point": "Pt",
    "Puente": "Puente",
    "Ranch Road": "Ranch Rd",
    "Ranch to Market Road": "RM",
    "Reservation Highway": "Resvn Hwy",
    "Road": "Rd",
    "Route": "Rte",
    "Row": "Row",
    "Rue": "Rue",
    "Ruta": "Ruta",
    "Sector": "Sec",
    "Sendero": "Sendero",
    "Service Road": "Svc Rd",
    "Skyway": "Skwy",
    "Square": "Sq",
    "State Forest Service Road": "St FS Rd",
    "State Highway": "State Hwy",
    "State Loop": "State Loop",
    "State Road": "State Rd",
    "State Route": "State Rte",
    "State Spur": "State Spur",
    "State Trunk Highway": "St Trunk Hwy",
    "Terrace": "Ter",
    "Town Highway": "Town Hwy",
    "Town Road": "Town Rd",
    "Township Highway": "Twp Hwy",
    "Township Road": "Twp Rd",
    "Trail": "Trl",
    "Tribal Road": "Tribal Rd",
    "Tunnel": "Tunl",
    "US Forest Service Highway": "USFS Hwy",
    "US Forest Service Road": "USFS Rd",
    "US Highway": "US Hwy",
    "US Route": "US Rte",
    "Vereda": "Ver",
    "Via": "Via",
    "Vista": "Vis",
}

# Prefix_Alternate constant maps alternate prefix street types to canonical abbreviations
Prefix_Alternate = {
    "Av": "Ave",
    "Aven": "Ave",
    "Avenu": "Ave",
    "Avenue": "Ave",
    "Avn": "Ave",
    "Avnue": "Ave",
    "Boul": "Blvd",
    "Boulv": "Blvd",
    "Bypa": "Byp",
    "Bypas": "Byp",
    "Byps": "Byp",
    "Crt": "Ct",
    "Exp": "Expy",
    "Expr": "Expy",
    "Express": "Expy",
    "Expw": "Expy",
    "Highwy": "Hwy",
    "Hiway": "Hwy",
    "Hiwy": "Hwy",
    "Hway": "Hwy",
    "Lanes": "Ln",
    "Loops": "Loop",
    "Plza": "Plz",
    "Sqr": "Sq",
    "Sqre": "Sq",
    "Squ": "Sq",
    "Terr": "Ter",
    "Tr": "Trl",
    "Trails": "Trl",
    "Trls": "Trl",
    "Tunel": "Tunl",
    "Tunls": "Tunl",
    "Tunnels": "Tunl",
    "Tunnl": "Tunl",
    "Vdct": "Via",
    "Viadct": "Via",
    "Viaduct": "Via",
    "Vist": "Vis",
    "Vst": "Vis",
    "Vsta": "Vis"
}

# Prefix_Type merges canonical and alternate prefix types
Prefix_Type = Map({**Prefix_Canonical, **Prefix_Alternate})

# Suffix_Canonical constant maps canonical street type suffixes to their abbreviations
Suffix_Canonical = {
    "Alley": "Aly",
    "Arcade": "Arc",
    "Avenida": "Ave",
    "Avenue": "Ave",
    "Beltway": "Beltway",
    "Boulevard": "Blvd",
    "Bridge": "Brg",
    "Bypass": "Byp",
    "Causeway": "Cswy",
    "Circle": "Cir",
    "Common": "Cmn",
    "Commons": "Cmns",
    "Corners": "Cors",
    "Court": "Ct",
    "Courts": "Cts",
    "Crescent": "Cres",
    "Crest": "Crst",
    "Crossing": "Xing",
    "Cutoff": "Cutoff",
    "Drive": "Dr",
    "Driveway": "Driveway",
    "Esplanade": "Esplanade",
    "Estates": "Ests",
    "Expressway": "Expy",
    "Forest Highway": "Forest Hwy",
    "Fork": "Frk",
    "Four-Wheel Drive Trail": "4WD Trl",
    "Freeway": "Fwy",
    "Grade": "Grade",
    "Heights": "Hts",
    "Highway": "Hwy",
    "Jeep Trail": "Jeep Trl",
    "Landing": "Lndg",
    "Lane": "Ln",
    "Logging Road": "Logging Rd",
    "Loop": "Loop",
    "Motorway": "Mtwy",
    "Oval": "Oval",
    "Overpass": "Opas",
    "Parkway": "Pkwy",
    "Pass": "Pass",
    "Passage": "Psge",
    "Path": "Path",
    "Pike": "Pike",
    "Place": "Pl",
    "Plaza": "Plz",
    "Point": "Pt",
    "Pointe": "Pointe",
    "Promenade": "Promenade",
    "Railroad": "RR",
    "Railway": "Rlwy",
    "Ramp": "Ramp",
    "River": "Riv",
    "Road": "Rd",
    "Roadway": "Roadway",
    "Route": "Rte",
    "Row": "Row",
    "Rue": "Rue",
    "Service Road": "Svc Rd",
    "Skyway": "Skwy",
    "Spur": "Spur",
    "Square": "Sq",
    "Stravenue": "Stra",
    "Street": "St",
    "Strip": "Strip",
    "Terrace": "Ter",
    "Thoroughfare": "Thoroughfare",
    "Tollway": "Tollway",
    "Trace": "Trce",
    "Trafficway": "Trfy",
    "Trail": "Trl",
    "Trolley": "Trolley",
    "Truck Trail": "Truck Trl",
    "Tunnel": "Tunl",
    "Turnpike": "Tpke",
    "Viaduct": "Viaduct",
    "View": "Vw",
    "Vista": "Vis",
    "Walk": "Walk",
    "Walkway": "Walkway",
    "Way": "Way",
}

# Suffix_Alternate constant maps alternate suffix street types to canonical abbreviations
Suffix_Alternate = {
    "Allee": "Aly",
    "Ally": "Aly",
    "Av": "Ave",
    "Aven": "Ave",
    "Avenu": "Ave",
    "Avenue": "Ave",
    "Avn": "Ave",
    "Avnue": "Ave",
    "Boul": "Blvd",
    "Boulv": "Blvd",
    "Brdge": "Brg",
    "Bypa": "Byp",
    "Bypas": "Byp",
    "Byps": "Byp",
    "Causway": "Cswy",
    "Circ": "Cir",
    "Circl": "Cir",
    "Crcl": "Cir",
    "Crcle": "Cir",
    "Crecent": "Cres",
    "Cresent": "Cres",
    "Crscnt": "Cres",
    "Crsent": "Cres",
    "Crsnt": "Cres",
    "Crssing": "Xing",
    "Crssng": "Xing",
    "Crt": "Ct",
    "Driv": "Dr",
    "Drv": "Dr",
    "Exp": "Expy",
    "Expr": "Expy",
    "Express": "Expy",
    "Expw": "Expy",
    "Freewy": "Fwy",
    "Frway": "Fwy",
    "Frwy": "Fwy",
    "Height": "Hts",
    "Hgts": "Hts",
    "Highwy": "Hwy",
    "Hiway": "Hwy",
    "Hiwy": "Hwy",
    "Ht": "Hts",
    "Hway": "Hwy",
    "La": "Ln",
    "Lanes": "Ln",
    "Lndng": "Lndg",
    "Loops": "Loop",
    "Ovl": "Oval",
    "Parkways": "Pkwy",
    "Parkwy": "Pkwy",
    "Paths": "Path",
    "Pikes": "Pike",
    "Pkway": "Pkwy",
    "Pkwys": "Pkwy",
    "Pky": "Pkwy",
    "Plza": "Plz",
    "Rivr": "Riv",
    "Rvr": "Riv",
    "Spurs": "Spur",
    "Sqr": "Sq",
    "Sqre": "Sq",
    "Squ": "Sq",
    "Str": "St",
    "Strav": "Stra",
    "Strave": "Stra",
    "Straven": "Stra",
    "Stravn": "Stra",
    "Strt": "St",
    "Strvn": "Stra",
    "Strvnue": "Stra",
    "Terr": "Ter",
    "Tpk": "Tpke",
    "Tr": "Trl",
    "Traces": "Trce",
    "Trails": "Trl",
    "Trls": "Trl",
    "Trnpk": "Tpke",
    "Trpk": "Tpke",
    "Tunel": "Tunl",
    "Tunls": "Tunl",
    "Tunnels": "Tunl",
    "Tunnl": "Tunl",
    "Turnpk": "Tpke",
    "Vist": "Vis",
    "Vst": "Vis",
    "Vsta": "Vis",
    "Walks": "Walk",
    "Wy": "Way",
}

# Suffix_Type merges canonical and alternate suffix types
Suffix_Type = Map({**Suffix_Canonical, **Suffix_Alternate})

# Unit_Type constant lists acceptable USPS unit type abbreviations
Unit_Type = Map({
    "Apartment": "Apt",
    "Basement": "Bsmt",
    "Building": "Bldg",
    "Department": "Dept",
    "Floor": "Fl",
    "Front": "Frnt",
    "Hangar": "Hngr",
    "Lobby": "Lbby",
    "Lot": "Lot",
    "Lower": "Lowr",
    "Office": "Ofc",
    "Penthouse": "Ph",
    "Pier": "Pier",
    "Rear": "Rear",
    "Room": "Rm",
    "Side": "Side",
    "Slip": "Slip",
    "Space": "Spc",
    "Stop": "Stop",
    "Suite": "Ste",
    "Trailer": "Trlr",
    "Unit": "Unit",
    "Upper": "Uppr",
})

# Std_Abbr merges all abbreviation types
Std_Abbr = Map({
    **Directional,
    **Prefix_Qualifier,
    **Suffix_Qualifier,
    **Prefix_Type,
    **Suffix_Type
})

# Name_Abbr constant maps common toponym abbreviations to their full word equivalents
Name_Abbr = Map({
    "Av": "Avenue",
    "Ave": "Avenue",
    "Blvd": "Boulevard",
    "Bot": "Bottom",
    "Boul": "Boulevard",
    "Boulv": "Boulevard",
    "Br": "Branch",
    "Brg": "Bridge",
    "Canyn": "Canyon",
    "Cen": "Center",
    "Cent": "Center",
    "Cir": "Circle",
    "Circ": "Circle",
    "Ck": "Creek",
    "Cnter": "Center",
    "Cntr": "Center",
    "Cnyn": "Canyon",
    "Cor": "Corner",
    "Cors": "Corners",
    "Cp": "Camp",
    "Cr": "Creek",
    "Crcl": "Circle",
    "Crcle": "Circle",
    "Cres": "Crescent",
    "Crscnt": "Crescent",
    "Ct": "Court",
    "Ctr": "Center",
    "Cts": "Courts",
    "Cyn": "Canyon",
    "Div": "Divide",
    "Dr": "Drive",
    "Dv": "Divide",
    "Est": "Estate",
    "Ests": "Estates",
    "Ext": "Extension",
    "Extn": "Extension",
    "Extnsn": "Extension",
    "Forests": "Forest",
    "Forg": "Forge",
    "Frg": "Forge",
    "Ft": "Fort",
    "Gatewy": "Gateway",
    "Gdn": "Garden",
    "Gdns": "Gardens",
    "Gtwy": "Gateway",
    "Harb": "Harbor",
    "Hbr": "Harbor",
    "Height": "Heights",
    "Hgts": "Heights",
    "Highwy": "Highway",
    "Hiway": "Highway",
    "Hiwy": "Highway",
    "Holws": "Hollow",
    "Ht": "Heights",
    "Hway": "Highway",
    "Hwy": "Highway",
    "Is": "Island",
    "Iss": "Islands",
    "Jct": "Junction",
    "Jction": "Junction",
    "Jctn": "Junction",
    "Junctn": "Junction",
    "Juncton": "Junction",
    "Ldg": "Lodge",
    "Lgt": "Light",
    "Lndg": "Landing",
    "Lodg": "Lodge",
    "Loops": "Loop",
    "Mt": "Mount",
    "Mtin": "Mountain",
    "Mtn": "Mountain",
    "Orch": "Orchard",
    "Parkwy": "Parkway",
    "Pk": "Park",
    "Pkway": "Parkway",
    "Pkwy": "Parkway",
    "Pky": "Parkway",
    "Pl": "Place",
    "Pnes": "Pines",
    "Pr": "Prairie",
    "Prr": "Prairie",
    "Pt": "Point",
    "Pts": "Points",
    "Rdg": "Ridge",
    "Riv": "River",
    "Rnchs": "Ranch",
    "Spg": "Spring",
    "Spgs": "Springs",
    "Spng": "Spring",
    "Spngs": "Springs",
    "Sq": "Square",
    "Squ": "Square",
    "Sta": "Station",
    "Statn": "Station",
    "Ste": "Sainte",
    "Stn": "Station",
    "Str": "Street",
    "Ter": "Terrace",
    "Terr": "Terrace",
    "Tpk": "Turnpike",
    "Tpke": "Turnpike",
    "Tr": "Trail",
    "Trls": "Trail",
    "Trpk": "Turnpike",
    "Tunls": "Tunnel",
    "Un": "Union",
    "Vill": "Village",
    "Villag": "Village",
    "Villg": "Village",
    "Vis": "Vista",
    "Vlg": "Village",
    "Vlgs": "Villages",
    "Wls": "Wells",
    "Wy": "Way",
    "Xing": "Crossing",
})

# State constant maps US state and territory names to their 2-letter USPS abbreviations
State = Map({
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Federated States of Micronesia": "FM",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Marshall Islands": "MH",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Palau": "PW",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
})
