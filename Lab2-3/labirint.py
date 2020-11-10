import random
import matplotlib.pyplot as plt

class point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def print(self):
        print(f'{self.x}, {self.y}')

def dist(p1,p2):
    return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

def dist_man(p1,p2):
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)

class state:

    def __init__(self,filename = None):
        if filename is None:
            self.m = 0
            self.n = 0
            self.lab = []
            self.start = point(0,0)
            self.fin = point(0,0)
            self.curr = self.start
            self.parent = None
            self.depth = 0
        else:
            self.lab = []
            with open(filename) as f:
                count = 0
                for line in f:
                    if count == 0: 
                        listt = [int(x) for x in line.split(" ")]
                        self.n, self.m = listt[0], listt[1]
                    elif count == 1:
                        listt = [int(x) for x in line.split(" ")]
                        xs, ys = listt[0], listt[1]
                        self.start = point(xs,ys)
                    elif count == 2:
                        listt = [int(x) for x in line.split(" ")]
                        xf, yf = listt[0], listt[1]
                        self.fin = point(xf,yf)
                    else:
                        self.lab.append([-int(c) for c in line[:-1]])

                    count += 1
                            
            self.curr = self.start
            self.mark(self.curr)
            #self.lab[self.fin.x][self.fin.y] = 2
            self.parent = None
            self.depth = 0
            
    def is_final(self):

        if(self.lab[self.fin.x][self.fin.y] == 1): return True, True

        for i in range(self.n):
            for j in range(self.m):
                if self.lab[i][j] == -1: continue
                if self.lab[i][j] == 1:
                    if i > 0 and self.lab[i-1][j] == 0: return False, False
                    if i < self.n and self.lab[i+1][j] == 0: return False, False
                    if j > 0 and self.lab[i][j-1] == 0: return False, False
                    if j < self.m and self.lab[i][j+1] == 0: return False, False

        return True, False

    def is_final_hc(self):

        if(self.lab[self.fin.x][self.fin.y] == 1): return True, True

        if len([i for i in range(4) if self.is_valid_trans_hc(i)]) == 0: return True, False

        return False, False

    def is_valid_trans(self,trans):
        i,j = self.curr.x, self.curr.y
        if trans == 0:
            if i <= 0: return False
            if self.lab[i-1][j] ==0: return True

        elif trans == 1:
            if j >= self.m-1: return False
            if self.lab[i][j+1] ==0: return True

        elif trans == 2:
            if i >= self.n-1: return False
            if self.lab[i+1][j] ==0: return True

        elif trans == 3:
            if j <= 0: return False
            if self.lab[i][j-1] ==0: return True

        return False
    
    def is_valid_trans_hc(self,trans):
        i,j = self.curr.x, self.curr.y
        if trans == 0:
            if i <= 0: return False
            if self.lab[i-1][j] ==0: 
                return dist(self.curr,self.fin) > dist(point(i-1,j),self.fin)

        elif trans == 1:
            if j >= self.m-1: return False
            if self.lab[i][j+1] ==0: 
                return dist(self.curr,self.fin) > dist(point(i,j+1),self.fin)

        elif trans == 2:
            if i >= self.n-1: return False
            if self.lab[i+1][j] ==0: 
                return dist(self.curr,self.fin) > dist(point(i+1,j),self.fin)

        elif trans == 3:
            if j <= 0: return False
            if self.lab[i][j-1] ==0: 
                return dist(self.curr,self.fin) > dist(point(i,j-1),self.fin)

        else: return False

    def apply_trans(self,trans):

        new_state = self.copy()
        i, j = new_state.curr.x, new_state.curr.y
        if(not self.is_valid_trans(trans)): return None

        if trans == 0:
            new_state.lab[i-1][j] = 1
            new_state.curr = point(i-1,j)

        elif trans == 1:
            new_state.lab[i][j+1] = 1
            new_state.curr = point(i,j+1)

        elif trans == 2:
            new_state.lab[i+1][j] = 1
            new_state.curr = point(i+1,j)

        elif trans == 3:
            new_state.lab[i][j-1] = 1
            new_state.curr = point(i,j-1)

        new_state.parent = self
        new_state.deph = self.depth+1
        return new_state

    def copy(self):

        copy = state()
        copy.m = self.m
        copy.n = self.n
        copy.start = self.start
        copy.fin = self.fin
        copy.curr = self.curr
        copy.lab = [x[:] for x in self.lab]

        return copy

    def mark(self,poz):
        self.lab[poz.x][poz.y] = 1

    def print(self):
        print(self.m,self.n)
        print("start point: ",end = "")
        self.start.print()
        print("finish point: ",end = "")
        self.fin.print()
        print("current point: ",end = "")
        self.curr.print()
        for i in range(self.m):
            for j in range(self.n):
                if self.lab[i][j] == -1:
                    print("#", end=" ")
                elif i == self.start.x and j == self.start.y:
                    print("s", end=" ")
                elif i == self.fin.x and j == self.fin.y:
                    print("X", end=" ")
                elif i == self.curr.x and j == self.curr.y:
                    print("*", end=" ")
                elif self.lab[i][j] == 0:
                    print(" ", end=" ")
                elif self.lab[i][j] == 1:
                    print(".", end=" ")
            print("")

    def heur_score(self):

        hc_neigh = [i for i in range(4) if self.is_valid_trans_hc(i)]

        if len(hc_neigh)>0: return dist_man(self.curr,self.fin)
        else: return dist_man(self.curr,self.fin) + 1

    def show_lab(self):

        backup = self.lab[self.fin.x][self.fin.y]
        self.lab[self.fin.x][self.fin.y] = 2
            
        plt.matshow(self.lab)
        plt.show()

        self.lab[self.fin.x][self.fin.y] = backup
            

def solve_bktr(state):
    possible_states = [state.apply_trans(i) for i in range(4) if state.is_valid_trans(i)]
    while(len(possible_states)):
        state = possible_states.pop()
        
        final,win = state.is_final()
        
        if(win):
            sol = []
            st_copy = state
            while(state is not None):
                sol += [state.curr]
                state = state.parent
            return sol[-1::-1], st_copy
        
        elif not final:
            possible_states += [state.apply_trans(i) for i in range(4) if state.is_valid_trans(i)]
        
        
        else: 
            return [],state
    

def solve_bfs(state):
    possible_states = [state.apply_trans(i) for i in range(4) if state.is_valid_trans(i)]
    queue = 0
    while(queue < len(possible_states)):
        state = possible_states[queue]
        queue += 1
        
        final,win = state.is_final()
        
        if(win):
            sol = []
            st_copy = state
            while(state is not None):
                sol += [state.curr]
                state = state.parent
            return sol[-1::-1], st_copy
        
        elif not final:
            possible_states += [state.apply_trans(i) for i in range(4) if state.is_valid_trans(i)]
        
        else: 
            return [],state
    

def solve_hc(state):

    possible_states = [state.apply_trans(i) for i in range(4) if state.is_valid_trans_hc(i)]
    while(len(possible_states)):
        state = possible_states.pop()
        
        final,win = state.is_final_hc()
        
        if win:
            sol = []
            st_copy = state
            while(state is not None):
                sol += [state.curr]
                state = state.parent
            return sol[-1::-1], st_copy
        
        elif not final:
            possible_states += [state.apply_trans(i) for i in range(4) if state.is_valid_trans_hc(i)]
        
        else: 
            return [], state

def solve_sa(state:state):

    temp = 100
    cold = 0.999

    while(temp>=2):

        state.curr.print()
        final,win = state.is_final()
        #print(final,win)
        #print("")

        if(win):
            sol = []
            st_copy = state
            while(state is not None):
                sol += [state.curr]
                state = state.parent
            return sol[-1::-1], st_copy

        elif not final:

            neighs = [(i,state.apply_trans(i)) for i in range(4) if state.is_valid_trans(i)]

            if state.parent is not None: neighs += [(-1,state.parent)]

            scores = [(i,st.heur_score() + st.depth) for i,st in neighs]

            scores.sort(key = lambda x: x[1])

            count = len(scores)

            #print(count)
            #print("")

            #state.print()
            #state.show_lab()

            sums = 0
            for i,s in scores: sums += s

            s_mean = sums/count
                        
            probs = [( i, ((s_mean-s)/temp + 1/count) ) for i,s in scores]

            if state.parent is not None:

                index = -1
                for c,p in enumerate(probs): 
                    if p[0] == -1: index = c

                if len(probs)>1:
                    factor = 0.5
                    corr = probs[index][1]*factor
                    print(f"corr = {corr}")
                    print("")
                    corr2 = corr/(len(probs)-1)

                    probs2 = [(i,p+corr2) if i!=-1 else (i,p-corr) for i,p in probs]
                    probs = probs2

            #print(probs)
            #print("")

            probss = [probs[0]]

            for i in range(1,len(probs)):
                probss.append( (probs[i][0],probss[i-1][1]+probs[i][1]) )

            #print(probss)
            #print("")

            p = random.random()

            #print(p)
            #print("")

            trans = -1

            for i,pr in probss:
                if p < pr:
                    trans = i
                    break

            #print(trans)
            #print("")
            
            #print(state)

            if trans == -1 and state.parent is not None: 
                tresh = 0.3 if state.heur_score() <= state.parent.heur_score() else 0.7 
                state = state.parent
                p = random.random()
                while p < tresh and state.parent is not None:
                    tresh = 0.3 if state.heur_score() <= state.parent.heur_score() else 0.7 
                    state = state.parent
                    p = random.random()

                continue

            state = state.apply_trans(trans)

            temp = temp*cold

            print(temp)
            print("")

        else:
            return [],state


    return [],state
        
if __name__ == "__main__":
    
    x = state("./Labs2-3/labirint.txt")
    x.print()

    for t in range(4):
        print(f'trans {t} is valid? {x.is_valid_trans(t)}')

    path, f_state = solve_sa(x)
    if(len(path) == 0):
        print("Sollution not found")
        f_state.print()
        f_state.show_lab()
    else:
        print("path found")
        for p in path: p.print()
        f_state.print()
        f_state.show_lab()

