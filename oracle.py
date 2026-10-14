import json, math

def pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0
def num(x): return isinstance(x,(int,float)) and math.isfinite(x)
def jround(x): return math.floor(x+0.5)
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def r1(x): return jround(x*10)/10
def r2(x): return jround(x*100)/100
def money(x): return f"{r2(x):.2f}"

RATES={"smoke":1,"225":1.5,"275":2,"350":2.5,"sear":3.5}

def burn_plan(setting):
    if setting not in RATES: return {"error":"pick a dial setting"}
    return {"rate":RATES[setting]}

def render_burn(r,setting):
    return ("Your "+setting+" dial figures about "+jsnum(r["rate"])
            +" lb of pellets an hour - a labeled norm; the auger tells the truth by morning.")

def cold_factor(t):
    if t<30: return 1.5
    if t<50: return 1.25
    return 1

def hopper_plan(hopperLb,setting,tempF):
    if not pos(hopperLb): return {"error":"the hopper must be above zero"}
    if setting not in RATES: return {"error":"pick a dial setting"}
    if not num(tempF): return {"error":"the temperature must be a number"}
    return {"hours":r1(hopperLb/(RATES[setting]*cold_factor(tempF))),"cold":cold_factor(tempF)}

def render_hopper(r,hopperLb,setting,tempF):
    s="Your "+jsnum(hopperLb)+" lb hopper at "+setting+" figures about "+jsnum(r["hours"])+" hours"
    if r["cold"]>1: s+=" on a "+jsnum(tempF)+" F evening - the cold eats from the same bag"
    return s+"."

def cost_plan(bagPrice,bagLb,hours,setting):
    if not pos(bagPrice) or not pos(bagLb) or not pos(hours):
        return {"error":"bag price, bag weight and hours must all be above zero"}
    if setting not in RATES: return {"error":"pick a dial setting"}
    burn=RATES[setting]*hours
    return {"burn":r1(burn),"cost":r2(burn/bagLb*bagPrice)}

def render_cost(r,bagPrice,bagLb,hours,setting):
    return ("Your "+jsnum(hours)+" hour cook at "+setting+" burns about "+jsnum(r["burn"])+" lb - $"
            +money(r["cost"])+" of a $"+money(bagPrice)+" bag, before the brisket.")

cases=[]
def add(tool,args):
    if tool=="burn": r=burn_plan(*args); fn=render_burn
    elif tool=="hopper": r=hopper_plan(*args); fn=render_hopper
    else: r=cost_plan(*args); fn=render_cost
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [("smoke",),("225",),("275",),("350",),("sear",)]:
    add("burn",a)
for a in [(20,"225",70),(20,"225",35),(18,"smoke",60),(20,"sear",75),(15,"275",25),(40,"225",45),(20,"350",10),(10,"smoke",48)]:
    add("hopper",a)
for a in [(14,20,12,"225"),(20,40,8,"275"),(18,20,4,"sear"),(14,20,16,"smoke"),(22,40,6,"350"),(15,20,10,"275"),(14,20,2,"225")]:
    add("cost",a)
add("burn",["high"]); add("hopper",[0,"225",70]); add("hopper",[20,"high",70]); add("cost",[0,20,12,"225"]); add("cost",[14,20,12,"grill"])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
