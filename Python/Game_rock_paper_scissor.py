import sys,random
print ('\033[0;32mRock,Paper,Scissor\033[0m')
# Variables
wins=0
losses=0
ties=0

while True:
        # History
        print('%s wins , %s losses, %s ties' % (wins,losses,ties))
        #User Move
        print('\033[0;32mChoose ur move ! [r,p,s,q]\033[0m')
        move = input()
        if move == 'q' :
            print('See u soon')
            sys.exit()
        elif move == 'r' :
            print('Rock VS...')
        elif move == 'p' :
            print('Paper VS....')
        elif move == 's' :
            print('Scissor VS...')
        else :
            print('wrong click !')
        
        #Comp Move
        ComChoise = random.randint(1,3)
        if ComChoise == 1 :
            print('Rock !')
            vs = 'r'
        elif ComChoise == 2 :
            print('Paper !')
            vs = 'p'
        elif ComChoise == 3 :
            print('Scissor !')
            vs = 's'
        
        # Status
        if vs == move :
            print('\033[0;32mLol it is a Tie ! :()\033[0m')
            ties = ties + 1
        elif ( vs == 'r' and move == 's' ) or (vs == 'p' and move == 'r' ) or (vs == 's' and move == 'p') :
            print('\033[0;32mI Won, Kidooo :)\033[0m')
            losses = losses +1 
        elif (vs =='r' and move == 'p') or (vs == 'p' and move =='s') or (vs == 's' and move == 'r') :
            print('\033[0;32mYou got me ,man :\'(\033[0m')
            wins = wins + 1
