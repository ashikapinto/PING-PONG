import socket, time, pickle, random

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("", 8008))
serversocket.listen(2)
arr = [400,400,400,400,0,0,0,0,0]
connection = []
ball_y_speed = 2
ball_x_speed = 2



def process_positions(array, player_1, player_2):
    #info[0] = key_up
    #info[1] = key_down
    global ball_y_speed, ball_x_speed
    #if array[8] == 1:
    

    '''PADDLE MOVING'''
    if player_1[0] == True:
        array[0]-=2
    else:
        array[0] = array[0]
    if player_1[1] == True:
        array[0]+=2
    else:
        array[0] = array[0]

    if player_2[0] == True:
        array[1]-=2
    else:
        array[1] = array[1]
    if player_2[1] == True:
        array[1]+=2
    else:
        array[1] = array[1]

    if array[0]<0:
        array[0] = 0
    elif array[0] > 540:
        array[0] = 540

    if array[1]<0:
        array[1] = 0
    elif array[1] > 540:
        array[1] = 540

    '''PADDLE MOVING'''

    '''BALL MOVING'''
    array[2] += round(ball_y_speed)
    array[3] += round(ball_x_speed)

    negative_speed = [-0.6, -0.65, -0.7, -0.75, -0.8, -0.85, -0.9, -0.95, -1]
    positive_speed = [-1, -1.05, -1.1, -1.15, -1.2, -1.25, -1.3, -1.35, -1.4, -1.45, -1.5]

    if array[2] > 595:
        if ball_y_speed >= 1:
            ball_y_speed *= -1
        elif ball_y_speed < 1:
            ball_y_speed *= -1
    if array[2] < 0:
        if ball_y_speed >= 1:
            ball_y_speed *= -1
        elif ball_y_speed < 1:
            ball_y_speed *= -1
    if array[3]>795:
        if ball_x_speed >= 1:
            ball_x_speed *= -1
        elif ball_x_speed < 1:
            ball_x_speed *= -1
        if ball_x_speed != 0 and ball_y_speed != 0:
            array[4] += 1
    if array[3]<0:
        if ball_x_speed >= 1:
            ball_x_speed *= -1
        elif ball_x_speed < 1:
            ball_x_speed *= -1
        if ball_x_speed != 0 and ball_y_speed !=0:
            array[5] += 1


    '''BALL MOVING'''


    '''PADDLE DETECTION'''
    if array[3]<20 and (array[0]<array[2] and array[0]+60>array[2]):
        ball_x_speed *=-1
    if array[3]>780 and (array[1]<array[2] and array[1]+60>array[2]):
        ball_x_speed *=-1

    #info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]
    if array[4] > 9:
        array[6] = 1
        ball_y_speed = 0
        ball_x_speed = 0
    elif array[5] > 9:
        array[7] = 1
        ball_y_speed = 0
        ball_x_speed = 0
    else:
        array[6] = 0
        array[7] = 0


    return array

def waiting_for_connections():
    while len(connection)<2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)

def receive_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


while True:
    waiting_for_connections()

    data_arr = pickle.dumps(arr)
    print(data_arr)
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    player1, player2 = receive_information()

    arr = process_positions(arr,player1, player2)
