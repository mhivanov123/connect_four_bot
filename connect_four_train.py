from connect_four_base import connect_four,c4_game,player
import json

p1 = player('X')
p2 = player('O')

for n in range(1000):
  board = connect_four()
  game = c4_game(board,p1,p2)
  game.play()

  board = connect_four()
  game = c4_game(board,p2,p1) 
  game.play()

  if n%50 == 0:
      p1.eve = n/1000
      p2.eve = n/1000

for state in p1.memory:
    p1.memory[state] = max([(key,value) for key,value in p1.memory[state].items()],key = lambda x: x[1])[0]

print(p1.memory['*'*42])
'''out_file = open("connect_four_optimal.json", "w") 
json.dump(p1.memory, out_file, indent = 6) 
out_file.close()'''
