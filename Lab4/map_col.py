countries = ["WA","SA","NT"]
colors = {
    "WA":{'r','g','b'},
    "SA":{'r','g'},
    "NT":{'g'}
}
neighbours = {
    "WA":["SA","NT"],
    "SA":["WA","NT"],
    "NT":["WA","SA"]
}

'''
T: {V}
WA: {NT, SA}
NT: {WA, Q, SA}
SA: {WA, NT, Q, NSW, V}
Q: {NT, SA, NSW}
NSW: {Q, SA, V}
V: {SA, NSW, T}
Mulțimea de culori asociată fiecărei regiuni:
WA: {red}, NT: {red, blue, green}, SA: {red, blue, green}, Q: {green}, NSW: {red, blue, green}, V:
{red, blue, green}, T: {red, blue, green}
'''

# countries = ["T","WA","NT","SA","Q","NSW","V"]
# colors = {
#     "WA":{'r'},
#     "NT":{'r','b','g'},
#     "SA":{'r','b','g'},
#     "Q":{'g'},
#     "NSW":{'r','b','g'},
#     "V":{'r','b','g'},
#     "T":{'r','b','g'}
# }
# neighbours = {
#     "T": ["V"],
#     "WA": ["NT", "SA"],
#     "NT": ["WA", "Q", "SA"],
#     "SA": ["WA", "NT", "Q", "NSW", "V"],
#     "Q": ["NT", "SA", "NSW"],
#     "NSW": ["Q", "SA", "V"],
#     "V": ["SA", "NSW", "T"],
# }

def arc_reduce(c1, c2, colors):

    change = False
    for i in list(colors[c1]):
        found = False
        for j in list(colors[c2]):
            if i!=j: 
                found = True
                break
        if not found:
            colors[c1].remove(i)
            change = True

    return change

def arc_cons(countries,colors,neighbours):

    queue = []
    index = 0
    for x in countries:
        for y in countries:
            if x==y: continue
            if (x,y) in queue: continue
            if x in neighbours[y] or y in neighbours[x]: queue.append((x,y))

    while index < len(queue):
        x,y = queue[index]
        index += 1

        if arc_reduce(x,y,colors):
            if len(colors[x]) == 0:
                return None
            else:
                queue += [(x,z) for z in neighbours[x] if z!=x and z!=y]

    return colors

print(arc_cons(countries,colors,neighbours))


