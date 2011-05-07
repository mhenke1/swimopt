#!/bin/python

import sys
import random
import getopt

swimmers = []
domain = []

def printsolution(vec):
	if swimcost(vec) >= 100000:
		print "keine Loesung gefunden"
	else:		 
		slots=[]
		for i in range(len(swimmers)): 
			slots+=[i]

		for i in range(len(vec)):
			x=int(vec[i])
			swimmer = swimmers[slots[x]];
			print swimmer[0], swimmer[1], swimmer[2], swimmer[3]
			# Remove this slot
			del slots[x]
			name = swimmer[0]
			for j in range(len(slots)):
				swimmer = swimmers[slots[j]]
				if swimmer[0] == name:
					del slots[j]
					break
		print swimcost(vec)

def swimcost(vec):
	slots=[]
	for i in range(len(swimmers)):
		slots+=[i]
		
	cost = 0
	numWomen = 0
	numBreast = 0
	
	for i in range(len(vec)):
		x=int(vec[i])
		swimmer = swimmers[slots[x]]
		swimcost = swimmer[3]
		if swimcost <= 0:
			cost += 100000;
		else:
			cost += swimmer[3]
			if swimmer[1] == 'w':
				numWomen+=1
			if swimmer[2] == 'b':
				numBreast+=1
			del slots[x]
			name = swimmer[0]
			for j in range(len(slots)):
				swimmer = swimmers[slots[j]]
				if swimmer[0] == name:
					del slots[j]
					break
	if numWomen <> 5:
		cost = cost + 100000;
	if numBreast < 5:
		cost = cost + 100000;
			
	return cost;

def geneticoptimize(domain,costf,popsize=1000,step=1,mutprob=0.2,elite=0.4,maxiter=50):
	# Mutation Operation
	def mutate(vec):
		i=random.randint(0,len(domain)-1)
		if random.random()<0.5 and vec[i]-step >= domain[i][0]:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		elif vec[i]+step <=domain[i][1]:
			return vec[0:i]+[vec[i]+step]+vec[i+1:]
		else:
			return vec

	# Crossover Operation
	def crossover(r1,r2):
		i=random.randint(1,len(domain)-2)
		return r1[0:i]+r2[i:]

	# Build the initial population
	pop=[]
	for i in range(popsize):
		vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)

	# How many winners from each generation?
	topelite=int(elite*popsize)

	# Main loop
	for i in range(maxiter):
		scores=[(costf(v),v) for v in pop]
		scores.sort()
		ranked=[v for (s,v) in scores]

		# Start with the pure winners
		pop=ranked[0:topelite]
		# Add mutated and bred forms of the winners
		while len(pop)<popsize:
			if random.random()<mutprob:
				# Mutation
				c=random.randint(0,topelite-1)
				cm = mutate(ranked[c])
				pop.append(mutate(ranked[c]))
			else:
				# Crossover
				c1=random.randint(0,topelite-1)
				c2=random.randint(0,topelite-1)
				co = crossover(ranked[c1],ranked[c2])
				pop.append(co)

		# Print current best score
		print scores[0][0]
	return scores[0][1]

def readInputFile(inputfile):
	global swimmers
	infile = file(inputfile, 'r')
	for line in infile.readlines():
		swimdata = line.strip().split(";")
		breastData = (swimdata[0], swimdata[1], 'b' , int(swimdata[2]))
		swimmers+=[breastData]
		freestyleData = (swimdata[0], swimdata[1], 'k' , int(swimdata[3]))
		swimmers+=[freestyleData]
	infile.close()
	
def usage():
    print "swim --data=<datafile>"

def main(argv):
	global domain
	try:
		opts, args = getopt.getopt(argv[1:], "d:h", ["data=", "help"])
	except getopt.GetoptError, err:
		print str(err)
		usage()                         
		sys.exit(2)
		
	datafile = ""

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-d", "--data"):
			datafile = arg

	if (datafile == ""):
		print "no data file"
		usage()
		sys.exit()

	readInputFile(datafile)
	# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
	domain += [(0,(len(swimmers))-(i*2)-1) for i in range(10)];
	printsolution(geneticoptimize(domain,swimcost))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
 
