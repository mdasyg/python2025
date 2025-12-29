#pong / 1972 by Atari
# Multiplayer version using network
# by Minas Dasygenis, mdasyg@ieee.org
# 2024

#if intelisense error: Ctrl+Shift+P clear cache, Ctrl+Shift+P select interpeter

import pygame
import socket
from Paddle import *
from Ball import *
####
#### NETWORKING CODE INIT START
####
import network  # Import the newly created network module

# Networking initialization code
mode = input("Start as server (s) or client (c)? ").strip().lower()
connection = None

pygame.init()  # Initialize pygame after receiving the start signal
debug=0

# Define the maximum score for the game to end
maxscore = 5


# Networking initialization for server mode
if mode == 's':
    connections = network.start_server_multi()
    if connections:  # Ensure connections were successfully established
        print("Network setup complete for server!")
        conn1, addr1 = connections[0]
        conn2, addr2 = connections[1]
        print("Both clients are connected. Starting game...")
    else:
        print("Failed to establish connections with clients.")
        exit(1)
elif mode == 'c':
    server_ip = input("Enter server IP address: ").strip()
    server_port = int(input("Enter server port (default 12345): ") or 12345)
    connection = network.start_client(server_ip, server_port)
    # Wait for the start signal from the server before initializing the game window
    #STEP4: Both wait for the start signal
    start_signal = ""
    while start_signal != "START_GAME":
        # If the received message is not START_GAME just print it and wait again.
        start_signal = network.receive_message(connection)
        if start_signal != "START_GAME":
            print(f"Received something but still waiting for start signal. Received: {start_signal}")
            
    if start_signal == "START_GAME":
        print("Server Reports: Both clients are connected. Starting the game...")
        #OK Ready to Start: Go go go!
        size = (700, 500)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("MyPong")
    # Ensure a connection was established
    if connection:
        print("Network setup complete!")
    else:
        print("Failed to establish a network connection.")
        exit(1)
        
      
        

    
####
#### NETWORKING CODE INIT END
####


#### NETWORKING CODE Confirm that data exchange is functioning properly START

#NOT REQUIRED ANY MORE
if debug==1:
 if connection:
    if mode == 's':
        #1st client
        print("Waiting for a message from a client...")
        message = network.receive_message(connection)
        print(f"Received from client: {message}")       
        response = "Hello, Client!"
        network.send_message(connection, response)
        print(f"Sent to client: {response}")
        #2nd Client
        print("Waiting for a message from a client...")
        message = network.receive_message(connection)
        print(f"Received from client: {message}")       
        response = "Hello, Client!"
        network.send_message(connection, response)
        print(f"Sent to client: {response}")
    elif mode == 'c':
        message = "Hello, Server!"
        network.send_message(connection, message)
        print(f"Sent to server: {message}")
        response = network.receive_message(connection)
        print(f"Received from server: {response}")

      
        
#### NETWORKING CODE Confirm that data exchange is functioning properly START        

# Speed of Ball
pixelsspeed=20


#RGB Definitions of colors
#https://rgbcolorcode.com/
BLACK=(0,0,0)
WHITE=(255,255,255)



scoreA = 0
scoreB = 0

#3 sections
#Capture & Process Events 
#Game Logic & Algorithm
#Update Screen (redraw sprites at their possitions)

main_loop = True #flag to indicate that we are working on main loop
#create object to track time to render FPS

#BOTH Server&Client execute this common code
#Create file 'paddle.py'
paddleA = Paddle(WHITE,10,100)
paddleA.rect.x=20
paddleA.rect.y=200

paddleB = Paddle(WHITE,10,100)
paddleB.rect.x = 670
paddleB.rect.y=200

ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195

#  Put all sprites inside a list
all_sprites_list=pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
clock=pygame.time.Clock()





#We will use a counter to increase difficulty
counter=1
while main_loop:
    clock.tick(60) #update the clock (framerate), called once
    #
    # NOT NEEDED here input handling, because we have seperate client mode
    #
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_w]:
    #    paddleA.moveUp(pixelsspeed)
    #if keys[pygame.K_s]:
    #    paddleA.moveDown(pixelsspeed)
    #if keys[pygame.K_UP]:
    #    paddleB.moveUp(pixelsspeed)
    #if keys[pygame.K_DOWN]:
    #    paddleB.moveDown(pixelsspeed)
    if mode == 's':
        try:
            # Increase ball speed every 100 iterations
            if counter % 100 == 0:
                ball.velocity[0] *= 1.1
                ball.velocity[1] *= 1.1
                print(f"Ball speed increased! New velocity: {ball.velocity}")

            # STEP3: Move the ball and check for collisions (server-side logic) -- START
            ball.update()
            #check bouncing ball on 4 borders
            if ball.rect.x >=690:
                scoreA+=1
                ball.velocity[0]=-ball.velocity[0]
            if ball.rect.x<=0:
                scoreB+=1
                ball.velocity[0]=-ball.velocity[0]
            if ball.rect.y>490:
                ball.velocity[1]=-ball.velocity[1]
            if ball.rect.y<0:
                ball.velocity[1]=-ball.velocity[1]
                
            #Detect collision between the ball and a paddle
            if pygame.sprite.collide_mask(ball,paddleA) or pygame.sprite.collide_mask(ball,paddleB):
                ball.bounce()
            # STEP3:  END
            
            
            # Receive data from Client A
            data_from_clientA = network.receive_data(conn1)
            # Receive data from Client B
            data_from_clientB = network.receive_data(conn2)
            
            
            if data_from_clientA:
                if debug==1:
                    print(f"Received from Player A: {data_from_clientA}")
                if data_from_clientA['action'] != 'no_action':
                    if data_from_clientA['action'] == 'moveUp':
                        paddleA.moveUp(pixelsspeed)
                    elif data_from_clientA['action'] == 'moveDown':
                        paddleA.moveDown(pixelsspeed)

            
            if data_from_clientB:
                if debug==1:
                    print(f"Received from Player B: {data_from_clientB}")
                if data_from_clientB['action'] != 'no_action':
                    if data_from_clientB['action'] == 'moveUp':
                        paddleB.moveUp(pixelsspeed)
                    elif data_from_clientB['action'] == 'moveDown':
                        paddleB.moveDown(pixelsspeed)

            # Check for game end conditions and send proper messages
            if scoreA == maxscore or scoreB == maxscore:
                # Send the game result to both clients
                result_message = "You won!" if scoreA == maxscore else "You lost!"
                network.send_data(conn1, {"result": result_message})
                network.send_data(conn2, {"result": "You won!" if scoreB == maxscore else "You lost!"})
                # print(f"Game over! {result_message}")
                main_loop = False  # Exit the game loop


            # Send updated game state to both clients
            #STEP3: Add ball possition also
            # Create and send the updated game state to both clients
            game_state = {
                'paddleA_y': paddleA.rect.y,
                'paddleB_y': paddleB.rect.y,
                'ball_x': ball.rect.x,
                'ball_y': ball.rect.y,
                'scoreA': scoreA,
                'scoreB': scoreB
            }
            network.send_data(conn1, game_state)
            network.send_data(conn2, game_state)
            counter=counter+1
            if debug==1:
                print(f"Moving to loop {counter}")
        except Exception as e:
            print(f"An error occurred during the game loop: {e}")
            break

    #The client mode starts here
    elif mode == 'c':
        try:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    main_loop=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x:
                        main_loop=False
            # Capture and send player movement input
            keys = pygame.key.get_pressed()
            action = None
            if keys[pygame.K_w]:
                action = 'moveUp'
            elif keys[pygame.K_s]:
                action = 'moveDown'
                
            # If no action is detected, send a dummy packet
            # *SOS* if we do not send a packet the server will be blocked waiting
            if action:
                client_data = {'action': action}
            else:
                client_data = {'action': 'no_action'}  # Dummy packet to indicate no input
            if debug==1:
                print(f"Sending data: {client_data}")  # Debug
            network.send_data(connection, client_data)

            # Receive and process game state updates
            game_state = network.receive_data(connection)
            if game_state:
                if debug==1:
                    print(f"Game state received: {game_state}")
                if "result" in game_state:
                    print(game_state["result"])
                    main_loop = False  # Exit the loop when the game ends
                else:
                    # Update local variables or display based on the received game state
                    #STEP3: Update Game State
                    # Update the game display based on received game state
                    paddleA.rect.y = game_state['paddleA_y']
                    paddleB.rect.y = game_state['paddleB_y']
                    ball.rect.x = game_state['ball_x']
                    ball.rect.y = game_state['ball_y']
                    scoreA = game_state['scoreA']
                    scoreB = game_state['scoreB']
                
                 # -- Game Logic

                all_sprites_list.update()
                screen.fill(BLACK) #background color of screen/ Redraw black
                #draw the net
                pygame.draw.line(screen, WHITE, [349,0],[349,500],5)
                all_sprites_list.draw(screen)
                
                font = pygame.font.Font(None,74)
                text = font.render(str(scoreA),1, WHITE)
                screen.blit(text, (250,10))
                text = font.render(str(scoreB),1, WHITE)
                screen.blit(text, (400,10))
    
            pygame.display.flip() #update the screen            

        except Exception as e:
            print(f"An error occurred during client operation: {e}")
            break
        
        







   
    
  
    

    
    
    


   

    
pygame.quit()
    


