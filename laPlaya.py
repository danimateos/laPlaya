import sys
import random
import time
import os

simultaneous = False # do shops move at the exact same time? 
sameSpot = True # can 2 shops occupy the same spot?
jump = False # do adjacent shops jump over each other? (dependent on sameSpot)

class Beach:
    LEFT =-1
    HERE = 0
    RIGHT= 1

    def __init__(self, *args):
        spots= 100
        self.shops = []
        minStep = 1./spots

        if len(args)==1:
            numberOfShops = int(args[0])
        else:
            numberOfShops = len(args)

        for i in range(numberOfShops):

            if len(args)>1:
                spot = float(args[i])
                
            else:
                spot= random.random()

            
            self.shops.append(Shop(self, spot, minStep))

        for i in range(numberOfShops):
            self.shops[i].look(Beach.HERE)

    def update(self):
        
        
        for shop in self.shops:
            shop.report()
            left = shop.look(Beach.LEFT)
            right= shop.look(Beach.RIGHT)
            #print left, right, '\n'

            if left > right:
                shop.move(Beach.LEFT)

            elif right > left:
                shop.move(Beach.RIGHT)

        shop.update()


    def render(self):
        #print '\n'
        copy= list(self.shops)
        copy.sort(key=lambda Shop:Shop.spot)
        marks = [x.getPosition() for x in copy]
        #print marks
        lineWidth = 80 

        for shop in self.shops:
            myPos= copy.index(shop)

            if myPos==0:
                left= 0
                right= marks[myPos]/2+ marks[myPos+1]/2
            elif myPos == len(marks)-1:
                left= marks[myPos-1]/2 +marks[myPos]/2
                right= 1
            else:
                left= marks[myPos-1]/2 +marks[myPos]/2
                right= marks[myPos]/2+ marks[myPos+1]/2
            point = shop.getPosition()

            cMark = int(round((lineWidth* point)))
            lMark = int(round((lineWidth* left)))
            rMark = int(round((lineWidth* right)))

            a= '.' * lMark
            b= '-' * (cMark-lMark)
            c= '#'
            d= '-' * (rMark-cMark)
            e= '.' * (lineWidth - rMark)
            
            line = a + b + c + d + e
            print line

        print '\n'

    def getShops(self):
        return self.shops

class Shop:
        
   
    def __init__(self, beach, spot, step):

        self.beach = beach
        self.step = step  
        self.spot = spot
        self.fitness = 0.

    def evalFitness(self, spot):

        shops = list(self.beach.getShops())
        possible= Shop(self.beach, spot, self.step)
        shops.remove(self)
        shops.append(possible)
        shops.sort(key=lambda Shop:Shop.spot)
        myPos= shops.index(possible)
        marks = [x.getPosition() for x in shops]

        if myPos==0:
            fitness= marks[myPos]/2+marks[myPos+1]/2
        elif myPos == len(marks)-1:
            fitness = 1- marks[myPos]/2 - marks[myPos-1]/2
        else:
            fitness= marks[myPos+1]/2 - marks[myPos-1]/2

        return fitness

    def getPosition(self):
        return self.spot

    def move(self, direction):

        self.spot += direction * self.step    

    def look(self, direction):
        
        fitness = self.evalFitness(self.spot + self.step * direction)
        
        return fitness 
    
    def update(self):
        self.fitness= self.evalFitness(self.spot)

    def report(self):
        
        print 'shop #' + str(self.beach.getShops().index(self)) + ' @ ' + str(self.spot) + ' owns ' + str(self.evalFitness(self.spot))
       




b = Beach(*sys.argv[1:])

while(True):
    #os.system('cls' if os.name == 'nt' else 'clear')
    b.update()
    b.render()
    time.sleep(0.03333)
