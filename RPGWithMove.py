import random
import math
import pickle
import time

global inventory
global quests
global m_hp
global mm_hp
global m_weapons
global weapons
global m_weapon
global m_move
global classe
global save
global m_name

m_hp = 50
mm_hp = 50
inventory = []
save = [[],[],[],''] #inventory, weapons, quests, m_weapon
m_quests = ['The Shiv']
quests = {'The Shiv':1}
Q_directions = {'The Shiv':{0:' ',1:'Talk to the Prisoner (⚲) and aquire a Shiv for the escape'},'poop':{0:'pee'}}
enemy = {'Prisoner':[25,['Shiv','Headbut','Heal'],['Shiv']], 'King Septumus':[1000,['blah','blah'],['Potion of Healing X']]} #sorts by NPC_name to give e_hp,e_moves, REWARD? (possibly more)
m_weapon = 'Fists'
m_weapons = ['Fists']
weapons = {'Fists':[10,None],'Shiv':[15,None],}

narration = {'The Shiv': "After facing off against the king himself, and failing, you are thrown in maximum security prison. You will need to find a way out, and get stronger, if you ever have any chance of defeating him."}

#Next Steps:
#1. fix start game, player shouldnt be allowed to use m_moves against prisoner when in the prison, should only be allowed aftee you speak with the wizard? or just after you escape you get your stuff back, but not your weapon.
#2. maybe import csv so i dont have to put all the dialogue here? but how do i have inputs then?

def start_game(): #where player chooses class and name
    global classe 
    global weapons 
    global m_weapon 
    global m_move 
    global quests 
    global inventory 
    global m_name 
    m_name = input("Enter your character's name: ")
    classe_select = input("Choose your class: 1-Warrior 2-Hunter 3-Mage: ")
    if classe_select == '1':
            classe = 'Warrior'
            m_move = 'Shield Bash'
            #m_weapon = 'Spiked Mace' [25,None]
    elif classe_select == '2':
            classe = 'Hunter'
            m_move = 'Piercing Arrow'
            #m_weapon = 'Sharpened Dagger' [25,None]
    elif classe_select == '3':
            classe = 'Mage'
            m_move = 'Spell of Absorbing'
            #m_weapon = 'Aprentice Staff' [25,None]
    else:
        start_game()
    print('Your name is '+m_name+' and you are a '+classe)
    confirm = input('Confirm and begin?: ')
    if confirm == 'yes':
        print("--------------")
        print(narration['The Shiv'])
        print('Quest added: The Shiv')
        time.sleep(5);
        movement([],1,5,"Prison Courtyard",[],2,[],None)
    else:
        start_game()

def movement(board,m_x,m_y,place,loote,loote_num,deade,deade_i): #board == [], m_x == player x postion, m_y == player y position, place == location which will change how board looks, keeps looted from before going into other functions so looted stays constant, if it is the first time in the area or not
    #Where all of the visuals of the game are held
    global inventory
    global m_quests
    global quests
    global m_weapon
    global m_weapons
    global m_hp
    global classe
    global save
    global m_name

    #item = {'Septums X':[random.randint(1,13),1000]}
    #item = {'Potion of Healing X':[1,10],'Potion of Attack X':[1,10]}
    item = {'Septums X':[random.randint(1,13),1000], 'Potion of Healing X':[1,10],'Potion of Attack X':[1,10]} #Sorts by loot then [1] == loot_num possibility, and [2] == max amount for inventory
    #item {'Common':{'Septums X':[1,1000], 'Potion of Healing X':[1,10],'Potion of Attack X':[1,10]},'Rare'{},'Legendary'{}}
    area = {'Prison Courtyard':[[7,2,30,20],[2,7,9,4],4,[6,7],[5,6],2,35,11],"King's Castle":[[6,6],[1,9],2,[10],[5],1,12,11]} #[0] == i_x list [1] == i_y list [2] == # of chests [3] == e_x list [4] == e_y list [5] == # of NPCs [6] == width of board
    NPC = {'Prison Courtyard':{6:['Prisoner','The Shiv', '⚲','friendly'],7:['Prisoner',None,'⚲','hostile']},"King's Castle":{10:['King Septumus', 'Kill the King', '♚','hostile']}} #[0] == i_x of npc [1] == NPC name [2] == quest associated [3] == NPC Icon
    e_x = area[place][3]
    e_y = area[place][4]
    i_x = area[place][0]
    i_y = area[place][1]
    w = area[place][6]
    w2 = w-2
    h = area[place][7]
    NPCs = area[place][5]
    chests = area[place][2]
    visual = True
    direction = []
    #loot_num are the different times movement() will be activated throughout the game, determining when to save and load...
    if loote_num == 1: # loot_num == 1 when battle is won or dialogue is completed
        looted = loote
        print('Saving...')
        save[0] == []
        for s in range(len(inventory)):
            save[0].append(inventory[s])
        save[1] = []
        for q in range(len(m_quests)):
            save[1].append(m_quests[q])
        save[2] = []
        for w in range(len(m_weapons)):
            save[2].append(m_weapons[w])
        save[3] = ''
        save[3]+=str(m_weapon)
        for e in range(len(deade)):
            if e == deade_i:
                deade[e] = True
    if loote_num == 2: #loot_num == 2 when moving into new area, but still alive
        looted = []
        deade = []
        for l in range(chests):
            looted.append(False)
        for e in range(NPCs):
            deade.append(False)
        m_x = 1
        m_y = 5
        print('Saving...')
        save[0] == []
        for s in range(len(inventory)):
            save[0].append(inventory[s])
        save[1] = []
        for q in range(len(m_quests)):
            save[1].append(m_quests[q])
        save[2] = []
        for w in range(len(m_weapons)):
            save[2].append(m_weapons[w])
        save[3] = ''
        save[3]+=str(m_weapon)
    if loote_num == 0: #loot_num == when battle is lost
        looted = []
        deade = []
        for l in range(chests):
            looted.append(False)
        for e in range(NPCs):
            deade.append(False)
        m_x = 1
        m_y = 5
        print('Loading..')
        inventory = save[0]
        m_quests = save[1]
        m_weapons = save[2]
        m_weapon = save[3]
    moving = True
    while visual == True:
        #The chunk of code with creates the display of the board, accounting for NPC location, chests locations, and player location:
        for i in range(h):
            board.append([' ']*w)
            board[i] = ['|']*1+[' ']*w2+['|']*1
            if i == 0:
                board[i] = [' ']*1+['-']*w2
            if i == h-1:
                board[i] = [' ']*1+['-']*w2
            for l in range(chests): #When player isnt on same line as chests:
                if i == i_y[l]:
                    if looted[l] == False:
                        board[i] = ['|']*1+[' ']*(i_x[l]-1)+['◘']*1+[' ']*(w2-i_x[l])+['|']*1
                    if looted[l] == True:
                        board[i] = ['|']*1+[' ']*(i_x[l]-1)+['⊡']*1+[' ']*(w2-i_x[l])+['|']*1
            for e in range(NPCs): #When player isn on same line as NPCs:
                if i == e_y[e]:
                    if deade[e] == False:
                        board[i] = ['|']*1+[' ']*(e_x[e]-1)+[NPC[place][e_x[e]][2]]*1+[' ']*(w2-e_x[e])+['|']*1
                    if deade[e] == True:
                        board[i] = ['|']*1+[' ']*(e_x[e]-1)+['☠']*1+[' ']*(w2-e_x[e])+['|']*1
            if i == m_y: #When player is on their own line, or on a line with chests or NPCs:
                board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1
                for e in range(NPCs): 
                    direction.append('') #Determining where player will be after dialogue or battle is over, based on their inital direction (repeated alot)
                    if m_y == e_y[e]+1 and e_x[e] == m_x:
                        direction[e] = 'd'
                    if m_y == e_y[e]-1 and e_x[e] == m_x:
                        direction[e] = 'u'
                    if m_y == e_y[e]: #When player is on same line as Npc
                        NPC_name = NPC[place][e_x[e]][0]
                        if m_x == e_x[e]-1:
                            direction[e] = 'l'
                        if m_x == e_x[e]+1:
                            direction[e] = 'r'
                        if m_x == e_x[e]:
                            if deade[e] == False: #When NPC is alive, player will either talk with NPC or immediately fight, depending on their hostility
                                moving = False
                                if NPC[place][e_x[e]][3] == 'friendly': #If NPC is friendly, Nplayer will start dialogue with NPC
                                    interact = input("Talk to "+NPC_name+'?: ') #Option for player to talk or not
                                    if interact == 'yes':
                                        print(' ')
                                        if direction[e] == 'l':
                                            print('left')
                                            m_x = m_x-1
                                        if direction[e] == 'r':
                                            m_x =m_x+1
                                        if direction[e] == 'u':
                                            m_y = m_y -1
                                        if direction[e] == 'd':
                                            m_y = m_y +1
                                        deade_i = e
                                        dialogue(place,NPC_name,NPC[place][e_x[e]][1],quests[NPC[place][e_x[e]][1]],m_x,m_y,looted,deade,deade_i)
                                        moving = True
                                    if interact == 'no':
                                        print("You walk away")
                                        print(' ')
                                        moving = True
                                        if direction[e] == 'l':
                                            m_x = m_x-1
                                        if direction[e] == 'r':
                                            m_x =m_x+1
                                        if direction[e] == 'u':
                                            m_y = m_y -1
                                        if direction[e] == 'd':
                                            m_y = m_y +1
                                if NPC[place][e_x[e]][3] == 'hostile': #If NPC is hostile, no dialogue will start, battle will begin
                                    print(NPC_name+' is hostile and going to attack!')
                                    ready = input('Are you ready to fight?: ')
                                    if ready == 'yes':
                                        deade_i = e
                                        if direction[e] == 'l':
                                            m_x = m_x-1
                                        if direction[e] == 'r':
                                            m_x =m_x+1
                                        if direction[e] == 'u':
                                            m_y = m_y -1
                                        if direction[e] == 'd':
                                            m_y = m_y +1
                                        battle(place,NPC_name,enemy[NPC_name][0],random.choice(enemy[NPC_name][2]),enemy[NPC_name][1],m_x,m_y,looted,NPC[place][e_x[e]][1],deade,deade_i)
                            if deade[e] == True: #When NPC is already defeated previously by player:
                                print(NPC_name+' is defeated')
                                print('')
                                if direction[e] == 'l':
                                        pass
                                if direction[e] == 'r':
                                        pass
                                if direction[e] == 'u':
                                        pass
                                if direction[e] == 'd':
                                        pass
                                moving = True
                        if m_x < e_x[e]: #What line will look like if NPC is left of NPC
                            if deade[e] == False:
                                board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(e_x[e]-m_x-1)+[NPC[place][e_x[e]][2]]*1+[' ']*(w2-e_x[e])+['|']*1
                            if deade[e] == True:
                                board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(e_x[e]-m_x-1)+['☠']*1+[' ']*(w2-e_x[e])+['|']*1
                        if m_x > e_x[e]: #What line will look like if NPC is right of NPC
                            if deade[e] == False:
                                board[i] = ['|']*1+[' ']*(e_x[e]-1)+[NPC[place][e_x[e]][2]]*1+[' ']*(m_x-e_x[e]-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1
                            if deade[e] == True:
                                board[i] = ['|']*1+[' ']*(e_x[e]-1)+['☠']*1+[' ']*(m_x-e_x[e]-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1
                for l in range(chests): #When player is on line with chest:
                    if m_y == i_y[l]:
                        if m_x == i_x[l]: #When player x is on chest x
                            if looted[l] == False: #Determines whether the chest has already been looted
                                moving = False
                                append = 0
                                loot = str(random.choice(list(item))) #Random item is given based on dictionary of items
                                loot_num = int(item[loot][0]) #Amount of the item given to player, coins are random numbers, potions are always 1
                                loot = loot+str(loot_num) #Now the item should look something like: "Septums X10"
                                print("Chest opened: You aquired "+str(loot))
                                print("Inventory: "+'['+str(" , ".join(inventory)+']'))
                                add_inventory = input("Keep items?: ")
                                if add_inventory == 'yes':
                                    if len(inventory) > 0:
                                        for j in range(len(inventory)): #These functions are to determine whether the player already has the item or not, and how much to add if they do or do not
                                            if loot[0:loot.find('X')+1] == inventory[j][0:inventory[j].find('X')+1]:
                                                    append +=1
                                                    if int(inventory[j][inventory[j].find('X')+1:len(inventory[j])])+loot_num > item[loot[0:loot.find('X')+1]][1]: #If loot_num should only be 1
                                                        inventory[j] = str(inventory[j][0:inventory[j].find('X')+1]+str(item[loot[0:loot.find('X')+1]][1])) #the last number will be added by 1
                                                    else: #If loot_num should be any number great then 1, add that:
                                                        inventory[j] = str(inventory[j][0:inventory[j].find('X')+1]+str(int(inventory[j][inventory[j].find('X')+1:len(inventory[j])])+loot_num))
                                                    print("Inventory: "+'['+str(" , ".join(inventory)+']'))
                                                    print(' ')
                                        if str(loot[0:loot.find('X')+1]) != inventory[j][0:inventory[j].find('X')+1]: #If loot doesnt equal anything in inventory
                                            append +=1 #append is added so new loot isnt appended into inventory more then once
                                            print(append)
                                            if append == 1: #This way loot wont be appended on every occasion that it doesnt equal inventory[j]
                                                inventory.append(loot) 
                                                print("Inventory: "+'['+str(" , ".join(inventory)+']'))
                                                print(' ')
                                            if append > 1: 
                                                pass
                                    if len(inventory) == 0: #If nothing in inventory, append new loot automatically
                                        inventory.append(loot)
                                        print("Inventory: "+'['+str(" , ".join(inventory)+']'))
                                        print(' ')
                                if add_inventory == 'no':
                                    print("Items discarded")
                                    print(' ')
                                moving = True
                            looted[l] = True
                        if looted[l] == False: #if it isnt looted print the board like so, depending on location of player:
                                if m_x == i_x[l]:
                                    board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1
                                if m_x < i_x[l]:
                                    board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(i_x[l]-m_x-1)+['◘']*1+[' ']*(w2-i_x[l])+['|']*1 
                                if m_x > i_x[l]:
                                    board[i] = ['|']*1+[' ']*(i_x[l]-1)+['◘']*1+[' ']*(m_x-i_x[l]-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1 
                        if looted[l] == True:
                                if m_x == i_x[l]:
                                    board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1
                                if m_x < i_x[l]:
                                    board[i] = ['|']*1+[' ']*(m_x-1)+['◉']*1+[' ']*(i_x[l]-m_x-1)+['⊡']*1+[' ']*(w2-i_x[l])+['|']*1               
                                if m_x > i_x[l]:
                                    board[i] = ['|']*1+[' ']*(i_x[l]-1)+['⊡']*1+[' ']*(m_x-i_x[l]-1)+['◉']*1+[' ']*(w2-m_x)+['|']*1 
        print(place)
        for i in range(h):
            if moving == True: #Only when moving is true will the board print
                print(" ".join([str(x) for x in board[i]]))
        if moving == True: #Only when moving is true will movement be allowed
            xy_input = input('↑ = w , ↓ = s , → = d , ← = a : ')
            print(' ')
            if xy_input == 'w':
                m_y-=1
            if xy_input == 's':
                m_y+=1
            if xy_input == 'd':
                m_x+=1
            if xy_input == 'a':
                m_x-=1
            if xy_input == 'i':
                print('Inventory: '+'['+str(" , ".join(inventory)+']'))
                print(' ')
            if xy_input == 'q': #To access quests/directions
                notebook = ''
                if len(m_quests) > 0:
                    for q in range(len(m_quests)): #In order for directions to print along with quest name, combining dictionary and list values:
                        directions = Q_directions[m_quests[q]][quests[m_quests[q]]]
                        if q < len(m_quests)-1:
                            notebook += str(m_quests[q]+' , '+directions+' | ')
                        if q == len(m_quests)-1:
                            notebook += str(m_quests[q]+' , '+directions)
                    print('Quests: '+'['+notebook+']')
                if len(m_quests) == 0:
                    print('Quests: '+'['+str(" , ".join(m_quests)+']'))
                print(' ')
            if xy_input == 'z': #o access weapons (different from inventory) and change primary weapon that will be used in battle:
                primary = input('Change primary weapon?: ')
                if primary == 'no':
                    print('All Weapons: '+'['+str(" , ".join(m_weapons)+']'))
                    print('Primary Weapon: '+m_weapon)
                    print(' ')
                if primary == 'yes':
                    print('All Weapons: '+'['+str(" , ".join(m_weapons)+']'))
                    pprimary = input('Which weapon?: ')
                    if pprimary not in m_weapons:
                        print("Couldn't find that weapon in your inventory")
                        pprimary = input('Which weapon?: ')
                    if pprimary in m_weapons:
                        m_weapon = pprimary
                        print('All Weapons: '+'['+str(" , ".join(m_weapons)+']'))
                        print('Primary Weapon: '+m_weapon)
                        print(' ')
                        
        
def dialogue(area,NPC,quest,Q_stage,m_x,m_y,loote,deade,deade_i): #area == place, quest == quest associated with dialogue (if there is one), loote/deade/deade_i == remebering dead and looted lists from movement
    #Dialogue function is very small because i will add as I create more quests:
    global inventory  
    global m_quests
    global quests
    global m_hp
    global mm_hp
    global m_weapons
    global weapons
    global m_weapon
    global classe
    global m_name
    if area == 'Prison Courtyard':
            if NPC == 'Prisoner':
                if quest == 'The Shiv':
                    if Q_stage == 1:
                        #quests[quest] = int(quests[quest]+1) deleted because battle adds to quest stage 
                        battle(area,NPC,enemy[NPC][0],'Shiv',enemy[NPC][1],m_x,m_y,loote,quest,deade,deade_i)
                    if Q_stage == 2:
                        print('Leave me alone, your top dog around here now ok?')
                        print("--------------")
                        movement([],m_x,m_y,'Prison Courtyard',loote,1,deade,deade_i)

def battle(area,e_name,em_hp,reward,e_moves,m_x,m_y,loote,quest,deade,deade_i): #area == place, e_name == NPC being battled, em_hp == max health of enemy,
    #reward == reward associated with NPC, e_moves == enemy moves, quest == quest associated with NPC, loote/deade/deade_i == remebering dead and looted lists from movement
    global inventory  
    global m_quests
    global quests
    global m_hp
    global mm_hp
    global m_weapons
    global weapons
    global m_weapon
    global m_move
    global classe
    global s_weapons
    global s_quests
    global save
    #Dictionaries of player moves, enemy moves, and effects that can happen to both enemy and players
    m_moves = {'Warrior':{'Shield Bash':[6,'dizzy']},
               'Hunter':{'Piercing Arrow':[10,'bleeding']},
               'Mage':{'Spell of Absorbing':[0,'absorbing']}}
    e_moves = {'Shiv':[10,'bleeding'],'Headbut':[5,None],'Heal':[0,'healing']}
    m_effect = {'dizzy':['You attack is down from dizziness',2,2,'neg'],'bleeding':['You take 10 damage from bleeding',2,2,'neg'],'burning':['You take 10 damage from burning',2,2,'neg'],'absorbing':[e_name+' absorbed 10 helth from you',2,2,'neg'],'attack':['Your attack stats are raised',2,2,'pos'],'healing':['You raised your health by 15 points',1,1,'pos'],'cleansing':['All active affects have been removed',1,1,'pos'],'restoration':['Your full health is restored',1,1,'pos']}
    e_effect = {'dizzy':[e_name+' attack is down from dizziness',2,2,'neg'],'bleeding':[e_name+' takes 10 damage from bleeding',2,2,'neg'],'burning':[e_name+' tokes 10 damage from burning',2,2,'neg'],'absorbing':['You absorbed 10 damage from '+e_name,2,2,'neg'],'attack':[e_name+' attack stats are raised',2,2,'pos'],'healing':[e_name+' raised their health by 15 points',1,1,'pos'],'cleansing':['All active affects have been removed',1,1,'pos'],'restoration':[e_name+"'s full health is restored",1,1,'pos']}
    m_hp = mm_hp #Player equals max player health, max player health is for restorartion and healing
    e_hp = em_hp #same for enemy ^^
    turns = 1 #Dictates whos move it is, enemy or player
    e_effects = [] #active enemy affects, appended in battle when effects are started
    m_effects = [] #same for player ^^
    m_effected = False 
    append = 0
    print("--------------")
    print('Your Battle against '+e_name+' has begun')
    print('You have '+str(m_hp)+' health')
    print(e_name+' has '+str(e_hp)+' health')
    print("--------------")
    while e_hp > 0 and m_hp > 0: #While health of both are above 0:
        while turns % 2 == 1:
                md_multiplier = []
                m_remove = []
                if m_effected == True:
                    for m in range(len(m_effects)):
                            if m_effect[m_effects[m]][1] == 0 and len(m_effects) > 0:
                                    m_effect[m_effects[m]][1] += m_effect[m_effects[m]][2] 
                                    print(m_effects[m][0].upper()+m_effects[m][1:len(m_effects[m])]+' stopped')
                                    m_remove.append(m_effects[m])
                            if len(m_remove) > 0:
                                for i in range(len(m_remove)):
                                    m_effects.remove(m_remove[i])
                    if len(m_effects) > 0:
                            for m in range(len(m_effects)):
                                if m_effect[m_effects[m]][1] > 0 and len(m_effects) > 0:
                                    print(m_effect[m_effects[m]][0])
                                    if m_effects[m] == 'bleeding' or m_effects[m] == 'burning' :
                                        m_hp -= 15
                                    if m_effects[m] == 'absorbing':
                                        m_hp -= 10
                                        e_hp += 10
                                    if m_effects[m] == 'attack':
                                        md_multiplier.append(1.5)
                                    if m_effects[m] == 'dizzy':
                                        md_multiplier.append(.7)
                                    m_effect[m_effects[m]][1] = m_effect[m_effects[m]][1]-1
                m_effected = False
                if m_hp == 0:
                    print('You have 1 health')
                if m_hp != 0:
                    if m_hp < 1:
                        print("--------------")
                        print(e_name+' defeated you!')
                        print('Restarting from last save...')
                        print("--------------")
                        movement([],m_x,m_y,area,None,0,deade,deade_i)
                    else:
                        print('You have '+str(m_hp)+' health')
                        if e_hp == 0 or e_hp < 1:
                            print("--------------")
                            print('You have defeated '+e_name)
                            if quest != None:
                                quests[quest] = int(quests[quest]+1)
                            if reward not in m_weapons:
                                print('You aquired '+reward+'!')
                                print("--------------")
                                m_weapons.append(reward)
                                print('Primary Weapon: '+m_weapon)
                                pprimary = input('Set '+reward+' as primary weapon?: ')
                                if pprimary == 'no':
                                    pass
                                if pprimary == 'yes':
                                    m_weapon = reward
                                    print('Primary Weapon: '+m_weapon)
                                print("--------------")
                            movement([],m_x,m_y,area,loote,1,deade,deade_i)
                d_multiplier = math.prod(md_multiplier)
                turn = input('1- '+m_weapon+' 2- '+m_move+' 3- '+'inventory: ')
                if turn == '3':
                    if len(inventory) == 0:
                            print('You have nothing in your inventory')
                            turns-=1
                    if len(inventory) > 0:
                        if len(inventory) == 1 and 'Septums' in inventory[0]:
                            print('You have nothing in your inventory')
                            turns-=1
                        else:
                            p_inventory = ''
                            for p in range(len(inventory)):
                                if 'Septums' not in inventory[p]:
                                    p_inventory += str(str(p+1)+'- '+inventory[p]+' ')
                            print('Inventory: '+p_inventory)
                            inti_turn = input('What item do you want to use?: ')
                            if inti_turn == 'None' or inti_turn == 'none':
                                    turns-=1
                            else:
                                    if str(inti_turn+'-') in p_inventory:
                                        int_turn = p_inventory.find(str(inti_turn)+'-')
                                        x_turn = ''
                                        for x in range(len(p_inventory)):
                                            if p_inventory[x] == 'X' and x > int_turn:
                                                if x_turn == '':
                                                    x_turn = x
                                                if x_turn != '':
                                                    pass
                                        i_turn = str(p_inventory[int_turn+3:x_turn-1])
                                        effect = (i_turn[i_turn.find('of')+3:len(i_turn)]).lower()
                                        if effect in m_effects: 
                                            if effect == 'attack':
                                                    print("Attack stats are already raised")
                                            turns-=1
                                        if effect not in m_effects:
                                            inventory_remove = []
                                            print('You used '+i_turn)
                                            for i in range(len(inventory)):
                                                if i_turn in inventory[i]: #problem line when inventory is potion of attack and potion of healing and you use attack 
                                                    inventory[i] = str(inventory[i][0:inventory[i].find('X')+1]+str(int(inventory[i][inventory[i].find('X')+1:len(inventory[i])])-1)) 
                                                    if str(int(inventory[i][inventory[i].find('X')+1:len(inventory[i])])) == '0':
                                                        inventory_remove.append(inventory[i])
                                            m_effects.append(effect)
                                        if len(inventory_remove) > 0:
                                            for r in range(len(inventory_remove)):
                                                inventory.remove(inventory_remove[r])
                            if len(m_effects) > 0:
                                for o in range(len(m_effects)):
                                    if 'healing' in m_effects[o] or 'cleansing' in m_effects[o] or 'restoration' in m_effects[o]:
                                            if m_effects[o] == 'healing':
                                                    if m_hp +15 < mm_hp+1:
                                                       m_hp+=15
                                                    if m_hp +15 > mm_hp:
                                                       m_hp = mm_hp
                                            if len(m_effects) > 0:
                                                if m_effects[o] == 'cleansing':
                                                    for m in range(len(m_effects)):
                                                        if m_effect[m_effects[m]][3] == 'neg':
                                                            m_effect[m_effects[m]][1] = m_effect[m_effects[m]][2]
                                                            m_effects.remove(m_effects[m])
                                            if len(m_effects) > 0:
                                                if m_effects[o] == 'restoration':
                                                        m_hp = mm_hp
                                                        m_effects.remove(m_effects[o])
                                            print(m_effect[m_effects[o]][0])
                                            m_effects.remove(m_effects[o])
                if turn == '1':
                    print('You used '+m_weapon)
                    if weapons[m_weapon][0] > 0:
                        print('You did '+str(int(weapons[m_weapon][0]*d_multiplier))+' damage')
                    if weapons[m_weapon][1] != None:
                        print('You caused '+weapons[m_weapon][1])
                        e_effects.append(weapons[m_weapon][1])
                    e_hp-=int(weapons[m_weapon][0]*d_multiplier)
                if turn == '2':
                    print('You used '+m_move)
                    if m_moves[classe][m_move][0] > 0:
                        print('You did '+str(int(m_moves[classe][m_move][0]*d_multiplier))+' damage')
                    if m_moves[classe][m_move][1] != None:
                        if m_moves[classe][m_move][1] not in e_effects:
                            print('You caused '+m_moves[classe][m_move][1])
                            e_effects.append(m_moves[classe][m_move][1])
                        else:
                            print(e_name+' is already '+m_moves[classe][m_move][1])
                    e_hp-=int(m_moves[classe][m_move][0]*d_multiplier)
                print("--------------")
                turns+=1
        while turns % 2 == 0:
                ed_multiplier = []
                for m in range(len(e_effects)):
                        if e_effect[e_effects[m]][1] > 0:
                            print(e_effect[e_effects[m]][0])
                            if e_effects[m] == 'bleeding':
                                m_hp-=15
                            if e_effects[m] == 'absorbing':
                                e_hp-=10
                                m_hp+=10
                            if e_effects[m] == 'dizzy':
                                ed_multiplier.append(.6)
                        e_effect[e_effects[m]][1] -= 1
                        if e_effect[e_effects[m]][1] == 0 or e_effect[e_effects[m]][1] < 0 and len(e_effects) > 0:
                            e_effect[e_effects[m]][1] +=e_effect[e_effects[m]][2]
                            print(e_effects[m][0].upper()+e_effects[m][1:len(e_effects[m])]+' stopped')
                            e_effects.remove(e_effects[m])
                if e_hp == 0:
                    print('You have defeated '+e_name)
                    if quest != None:
                            quests[quest] = int(quests[quest]+1)
                    if reward not in m_weapons:
                            print('You aquired '+reward+'!')
                            print("--------------")
                            m_weapons.append(reward)
                            print('Primary Weapon: '+m_weapon)
                            pprimary = input('Set '+reward+' as primary weapon?: ')
                            if pprimary == 'no':
                                pass
                            if pprimary == 'yes':
                                m_weapon = reward
                                print('Primary Weapon: '+m_weapon)
                            print("--------------")
                    movement([],m_x,m_y,area,loote,1,deade,deade_i)
                if e_hp != 0:
                    if e_hp < 1:
                        #print("--------------")
                        print('You have defeated '+e_name)
                        if quest != None:
                            quests[quest] = int(quests[quest]+1)
                        if reward not in m_weapons:
                            print('You aquired '+reward+'!')
                            print("--------------")
                            m_weapons.append(reward)
                            print('Primary Weapon: '+m_weapon)
                            pprimary = input('Set '+reward+' as primary weapon?: ')
                            if pprimary == 'no':
                                pass
                            if pprimary == 'yes':
                                m_weapon = reward
                                print('Primary Weapon: '+m_weapon)
                        print("--------------")
                        movement([],m_x,m_y,area,loote,1,deade,deade_i)
                    else:
                        print(e_name+' has '+str(e_hp)+' health')
                        if m_hp == 0 or m_hp < 0:
                            print("--------------")
                            print(e_name+' defeated you!')
                            print('Restarting from last save...')
                            print("--------------")
                            movement([],m_x,m_y,area,None,0,deade,deade_i)
                d_multiplier = math.prod(ed_multiplier)
                turn = random.choice(list(enemy[e_name][1]))
                print(e_name+' used '+turn)
                if e_moves[turn][0] > 0:
                        print(e_name+' did '+str(int(e_moves[turn][0]*d_multiplier))+' damage')
                if e_moves[turn][1] != None:
                        if e_effect[e_moves[turn][1]][3] == 'neg':
                            if e_moves[turn][1] not in m_effects:
                                print(e_name+' caused '+e_moves[turn][1])
                                m_effects.append(e_moves[turn][1])
                        if e_effect[e_moves[turn][1]][3] == 'pos':
                            e_effects.append(e_moves[turn][1])
                            for o in range(len(e_effects)):
                                if 'healing' in e_effects or 'cleansing' in e_effects or 'restoration' in e_effects:
                                    if e_effects[o] == 'healing':
                                        if e_hp +15 < em_hp+1:
                                           e_hp+=15
                                        if e_hp +15 > em_hp:
                                           e_hp = em_hp
                                        print(e_effect[e_effects[o]][0])
                                    if e_effects[o] == 'cleansing':
                                        for m in range(len(e_effects)):
                                            if e_effect[m_effects[m]][3] == 'neg':
                                                e_effect[m_effects[m]][1] = e_effect[e_effects[m]][2]
                                                e_effects.remove(e_effects[m])
                                        print(e_effect[e_effects[o]][0])
                                    if e_effects[o] == 'restoration':
                                            e_hp = em_hp
                                            print(e_effect[e_effects[o]][0])
                                    e_effects.remove(e_effects[o])
                m_hp-=int(e_moves[turn][0]*d_multiplier)
                print("--------------")
                turns+=1
                m_effected = True
        if e_hp == 0 or e_hp < 0:
            print("--------------")
            print('You have defeated '+e_name)
            if quest != None:
                quests[quest] = int(quests[quest]+1)
            if reward not in m_weapons:
                print('You aquired '+reward+'!')
                print("--------------")
                m_weapons.append(reward)
                print('Primary Weapon: '+m_weapon)
                pprimary = input('Set '+reward+' as primary weapon?: ')
                if pprimary == 'no':
                    pass
                if pprimary == 'yes':
                    m_weapon = reward
                    print('Primary Weapon: '+m_weapon)
                print("--------------")
            movement([],m_x,m_y,area,loote,1,deade,deade_i)
        if m_hp == 0 or m_hp < 0:
            print("--------------")
            print(e_name+' defeated you!')
            print('Restarting from last save...')
            print("--------------")
            movement([],m_x,m_y,area,None,0,deade,deade_i)  
start_game()

