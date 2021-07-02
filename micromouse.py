import cv2
import numpy as np
import math
import sim
import sys
import time

client_id=-1

def isolatemaze(input_img):
    """
    -------------------
    Takes an image  as input, crops the image to isolate the maze

    Input Arguments:
    input_img- image in the form of an array

    Returns:
    croped_img- image of the isolated maze
    -------------------
    """

    gray=cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    ret,binary=cv2.threshold(gray,60,255,cv2.THRESH_BINARY)
    y,x=binary.shape
    y2=int(y/2)
    x2=int(x/2)

    for i in range(x-1):
        if binary[y2,i]==0:
            xi=i
            break

    for i in range(x-1,0,-1):
        if binary[y2,i]==0:
            xf=i
            break

    for i in range(y-1):
        if binary[i,x2]==0:
            yi=i
            break

    for i in range(y-1,0,-1):
        if binary[i,x2]==0:
            yf=i
            break
    
    binary=binary[yi-2:yf+2,xi-2:xf+2]
    croped_img=binary

    return croped_img


def encode_maze(croped_img):

    """
    -------------------
    Takes croped maze image  as input, returns a 2D array which  represents each cell of the maze

    Input Arguments:
    croped_img- maze image in the form of an array

    Returns:
    maze_array- encoded 2D array
    -------------------
    """

    maze_array=[]
    Y,X=croped_img.shape

    xstep=int(X/10)         #10 coz its a 10x10 maze
    ystep=int(Y/10)

    arr=np.zeros((10,10),dtype=int)

    xstart=int(xstep/2)
    ystart=int(ystep/2)
    xend=int(xstart+(9.2*xstep))
    yend=int(ystart+(9.2*ystep))

    for i in range(10):
        if i==0:
            arr[0][i]=3
            arr[9][i]=9
            arr[i][9]=6
            arr[9][9]=12
        elif i>0 and i<9:
            arr[0][i]=2
            arr[i][0]=1
            arr[i][9]=4
            arr[9][i]=8


    i=ystart
    I=-1
    while(i<yend):
        j=xstart
        I=I+1
        while j<xend:
            if croped_img[i,j]==0:
                q=(j/Y)*10
                J=round(q)-1
                arr[I][J]=arr[I][J]+4
                arr[I][J+1]=arr[I][J+1]+1
                j=j+10
            j=j+1
        i=i+ystep

    j=xstart
    J=-1
    while j<xend:
        i=ystart
        J=J+1
        while i<yend:
            if croped_img[i,j]==0:
                q=(i/X)*10
                I=round(q)-1
                arr[I][J]=arr[I][J]+8
                arr[I+1][J]=arr[I+1][J]+2
                i=i+10
            i=i+1
        j=j+xstep

    maze_array=arr.tolist()

    return maze_array


def find_path(maze_array, start_coord, end_coord):

        """
        ---------------
        Calculates the path in maze between the start coordinates and end coordinates

        Input Arguments:
        maze_array- encoded maze in the form of a 2D array

        start_coord- start coordinates of the path(row number,column number)

        end_coord- end coordinates of the path(row number,column number)
        
        Returns:
        path-path between start and end coordinates
        ---------------
        """

        path = None
        path=[]
        arr=maze_array
        import math
        def h(x1, y1):
                x2=end_coord[0]
                y2=end_coord[1]
                return abs(x1 - x2) + abs(y1 - y2)


        def pathh(came_from, current):
            start=start_coord[1]+(10*start_coord[0])
            a=(end_coord[0],end_coord[1])
            path.append(a)
            while current!=start:
                current = came_from[current]
                j=current%10
                i=((current-j)/10)
                if(i<=0):
                        i=0
                else:
                        i=math.floor(i)
                a=(i,j)
                path.append(a)
                #print(i,j)
            path.reverse()
            #print(path)
            
                
        def algorithm():
            count=0
            start=start_coord[1]+(10*start_coord[0])
            end=end_coord[1]+(10*end_coord[0])
            open_set =[]
            open_set.append((0, count, start))
            came_from = {}
            g_score={}
            f_score={}
            g_score[start] = 0
            f_score[start] = h(start_coord[0],start_coord[1])
            open_set_hash ={start}
            #open_set_hash.remove(1)
            for i in range(100):
                    if i!=start:
                        g_score[i]=100
            while len(open_set):

                current = min(open_set)[2]
                #print(current)
                #print(open_set_hash)
                open_set_hash.remove(current)
                #print(open_set)
                open_set.remove(min(open_set))
                if current == end:
                    #print('done')
                    pathh(came_from,end)
                    #end.make_end()
                    break

                else:
                                #L
                                #j-= 1
                                #co ord to cellno
                                #cell_no=j+(4*i)
                    #print('p')
                    j=current%10
                    i=((current-j)/10)
                    if(i<=0):
                        i=0
                    else:
                        i=math.floor(i)
                    #print(i,j)
                    x1=i
                    y1=j         
                    if (current%10):
                                    neighbor=current-1
                                    if not(arr[i][j-1]>3 and arr[i][j-1]<8 or arr[i][j-1]>11):
                                        temp_g_score = g_score[current] + 1
                                        if temp_g_score < g_score[neighbor]:
                                            came_from[neighbor] = current
                                            g_score[neighbor] = temp_g_score
                                            x1=x1-1
                                            f_score[neighbor] = temp_g_score + h(x1,y1)
                                            if neighbor not in open_set_hash:
                                                count += 1
                                                open_set.append((f_score[neighbor], count, neighbor))
                                                open_set_hash.add(neighbor)
                            
                                #R                
                    if ((current+1)%10):
                                    neighbor=current+1
                                    if not(arr[i][j+1]%2==1):
                                        #print('ok')
                                        temp_g_score = g_score[current] + 1
                                        #print(temp_g_score,g_score[neighbor])
                                        if temp_g_score < g_score[neighbor]:
                                            came_from[neighbor] = current
                                            g_score[neighbor] = temp_g_score
                                            x1=x1+1
                                            f_score[neighbor] = temp_g_score + h(x1,y1)
                                            
                                            if neighbor not in open_set_hash:
                                                count += 1
                                                open_set.append((f_score[neighbor], count, neighbor))
                                                open_set_hash.add(neighbor)
                                                #print(open_set_hash,open_set)

                                #U
                    if (current>9):
                                    neighbor=current-10
                                    if not(arr[i-1][j]>7 ):
                                        temp_g_score = g_score[current] + 1
                                        if temp_g_score < g_score[neighbor]:
                                            came_from[neighbor] = current
                                            g_score[neighbor] = temp_g_score
                                            y1=y1-1
                                            f_score[neighbor] = temp_g_score + h(x1,y1)
                                            if neighbor not in open_set_hash:
                                                count += 1
                                                open_set.append((f_score[neighbor], count, neighbor))
                                                open_set_hash.add(neighbor)


                                #D
                    if (current<90):
                                    neighbor=current+10
                                    
                                    #print(current,i)
                                    if not(arr[i+1][j]==2 or arr[i+1][j]==3 or arr[i+1][j]==6 or arr[i+1][j]==7 or arr[i+1][j]==10 or arr[i+1][j]==11 or arr[i+1][j]==14):
                                        temp_g_score = g_score[current] + 1
                                        if temp_g_score < g_score[neighbor]:
                                            came_from[neighbor] = current
                                            g_score[neighbor] = temp_g_score
                                            y1=y1+1
                                            f_score[neighbor] = temp_g_score + h(x1,y1)
                                            if neighbor not in open_set_hash:
                                                count += 1
                                                open_set.append((f_score[neighbor], count, neighbor))
                                                open_set_hash.add(neighbor)

        algorithm()

        if(len(path)==0):
                path=None
        return path


def init_remote_api_server():

        """
        ---------------------
        Closes any open connections and then starts communication thread with VREP software

        Returns:
        client_id- the client_id generated from start connection remote API
        ---------------------   
        """

        global client_id
        sim.simxFinish(-1) #closing all opened connections
        #starting communication with server
        client_id=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim

        return client_id



def send_data(maze_array):
        
        """
        --------------------
        Sends encoded maze data to VREP for generating the maze in VREP

        Input Arguments:
        maze_array- encoded maze in the form of a 2D array
        
        Returns:
        return_code- code returned by VREP
        ----------------------
        """

        global client_id
        return_code = -1

        #conversion of list to array
        arr=np.asarray(maze_array)
        #conversion to 1D array
        arr=arr.reshape(-1)
        emptybuff=bytearray()
        #calling function receivedata in server side by giving
        #maze array as input
        return_code,outInts,outFloats,outStrings,outBuffer=sim.simxCallScriptFunction(
        client_id,'Base',sim.sim_scripttype_customizationscript
                        ,'receiveData',arr,[],[],emptybuff
                         ,sim.simx_opmode_blocking)     

        return return_code


def exit_remote_api_server():
        
        """
        Closes the connection and then ends the communication with VREP

        """

        global client_id

        #closing the connection
        sim.simxGetPingTime(client_id)
        sim.simxFinish(client_id)

def vrep_path(path):
    """
    --------------------
    Converts the path which is in [row,column] format to co-ordinates in VREP

    Input arguments:
    path- path in the form of co ordinates from start to end

    Returns:
    path_vrep- path in vrep co-ordinates
    --------------------
    """
    length=len(path)
    path_vrep=[]
    for i in range(length):
        x_cord=(path[i][1]*0.36)+0.18
        y_cord=((9-path[i][0])*0.36)+0.18
        cord=(x_cord,y_cord)
        path_vrep.append(cord)

    return path_vrep




def traverse_path(path):

    """
    --------------------
    Starts the simulation in VREP then controls the motor speed and makes the bot 
    traverse the path from start to end

    Input arguments:
    path- path in the form of co ordinates from start to end

    --------------------
    """

    #getting object handles of bot,left motor and right motor
    res, bot= sim.simxGetObjectHandle(client_id, 'Diff_Drive_Bot', sim.simx_opmode_blocking)
    res, rjr= sim.simxGetObjectHandle(client_id, 'right_joint', sim.simx_opmode_blocking)
    res, rjl= sim.simxGetObjectHandle(client_id, 'left_joint', sim.simx_opmode_blocking)

    #starting simulation 
    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)


    if ((return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok)):
        print('\nSimulation started correctly in CoppeliaSim.')
        sim.simxGetPingTime(client_id)
        #getting initial position and orientation of bot
        rc,position=sim.simxGetObjectPosition(client_id,bot,-1,sim.simx_opmode_streaming)
        rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_streaming)
        while position[0]==0:    
            rc,position=sim.simxGetObjectPosition(client_id,bot,-1,sim.simx_opmode_buffer)
            rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)
            # print(position)

    
        length=len(path)
        check=0
        #to know along which axis the bot is alligned at any instant
        alongy=1
        alongx=0
        #loop which runs till all the points in the path is reached
        while check<length-1:
            current_x=path[check][0]
            current_y=path[check][1]
            next_x=path[check+1][0]
            next_y=path[check+1][1]

            if current_x>next_x and alongy==1:
                print('west')

                while not(abs(orientation[2])>3.11):                                                                         
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,-1,sim.simx_opmode_oneshot)
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)      
                alongx=-1
                alongy=0
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            elif current_x<next_x and alongy==1:
                print('east')

                while not(orientation[2]>-0.03 and orientation[2]<0.03 and orientation[2]!=0):                                                      
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,-1,sim.simx_opmode_oneshot)  
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)    
                alongx=1
                alongy=0
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            elif current_y<next_y and alongx==1:
                print('north')

                while not(orientation[2]<1.6 and orientation[2]>1.54):                                                       
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,-1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,1,sim.simx_opmode_oneshot)
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)      
                alongx=0
                alongy=1
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            elif current_y>next_y and alongx==1:
                print('south')

                while not(orientation[2]>-1.6 and orientation[2]<-1.54):                                                           
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,-1,sim.simx_opmode_oneshot) 
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)     
                alongx=0
                alongy=-1
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)


            elif current_x>next_x and alongy==-1:
                print('west')

                while not(abs(orientation[2])>3.11):                                                        
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,-1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,1,sim.simx_opmode_oneshot)
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)      
                alongx=-1
                alongy=0
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            # print(position[1],next_ysoft)
            elif current_x<next_x and alongy==-1:
                print('east')
                # time.sleep(15)

                while not(orientation[2]>-0.03 and orientation[2]<0.03 and orientation[2]!=0):                                                      
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,-1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,1,sim.simx_opmode_oneshot)  
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)    
                alongx=1
                alongy=0
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            elif current_y<next_y and alongx==-1:
                print('north')

                while not(orientation[2]<1.6 and orientation[2]>1.54):                                                      
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,-1,sim.simx_opmode_oneshot)
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)      
                alongx=0
                alongy=1
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)

            elif current_y>next_y and alongx==-1:
                print('south')

                while not(orientation[2]>-1.6 and orientation[2]<-1.54):                                                                         
                    rc=sim.simxSetJointTargetVelocity(client_id,rjl,-1,sim.simx_opmode_oneshot)
                    rc=sim.simxSetJointTargetVelocity(client_id,rjr,1,sim.simx_opmode_oneshot) 
                    rc,orientation=sim.simxGetObjectOrientation(client_id,bot,-1,sim.simx_opmode_buffer)     
                alongx=0
                alongy=-1
                rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)


            while abs(next_y-position[1])>0.02 and alongy:
                rc,position=sim.simxGetObjectPosition(client_id,bot,-1,sim.simx_opmode_buffer)
              
                if position[0]<current_x-0.01:
                    if alongy==1:
                        # print('lean left')
                        lspeed=1.5+0.5
                        rspeed=1
                    else:
                        # print('lean right')
                        rspeed=1.5+0.5
                        lspeed=1.5                                                       

                elif position[0]>current_x+0.01:
                    
                    if alongy==1:
                        # print('lean right')
                        rspeed=1.5+0.5
                        lspeed=1.5
                    else:
                        # print('lean left')
                        lspeed=1.5+0.5
                        rspeed=1.5                                                       
                else:
                    rspeed=1.5
                    lspeed=1.5

                rc=sim.simxSetJointTargetVelocity(client_id,rjr,rspeed,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,lspeed,sim.simx_opmode_oneshot)

            while abs(next_x-position[0])>0.02 and alongx:
                rc,position=sim.simxGetObjectPosition(client_id,bot,-1,sim.simx_opmode_buffer)
                
                if position[1]>current_y+0.01:
                    if alongx==1:
                        # print('lean left')
                        lspeed=2+0.5
                        rspeed=2
                    else:
                        # print('lean right')
                        rspeed=2+0.5
                        lspeed=2
                elif position[1]<current_y-0.01:
                    if alongx==1:
                        # print('lean right')
                        rspeed=2+0.5
                        lspeed=2
                    else:
                        # print('lean left')
                        lspeed=2+0.5
                        rspeed=2
                else:
                    rspeed=2
                    lspeed=2

                rc=sim.simxSetJointTargetVelocity(client_id,rjr,rspeed,sim.simx_opmode_oneshot)
                rc=sim.simxSetJointTargetVelocity(client_id,rjl,lspeed,sim.simx_opmode_oneshot)




            rc=sim.simxSetJointTargetVelocity(client_id,rjr,0,sim.simx_opmode_oneshot)
            rc=sim.simxSetJointTargetVelocity(client_id,rjl,0,sim.simx_opmode_oneshot)
            check=check+1




def main():

        # Initiate the Remote API connection with CoppeliaSim server
        print('\nConnection to CoppeliaSim Remote API Server initiated.')
        print('Trying to connect to Remote API Server...')

        try:
                client_id = init_remote_api_server()

                if (client_id != -1):
                        print('\nConnected successfully to Remote API Server in CoppeliaSim!')
                
                else:
                        print('\n[ERROR] Failed connecting to Remote API server!')
                        sys.exit()

        except Exception:
                sys.exit()
        
        path=r"test_cases\maze06.jpg"
        image=cv2.imread(path)
        croped_img=isolatemaze(image)
        maze_array=encode_maze(croped_img)
        # print(maze_array)
        path=find_path(maze_array,(9,0),(0,9))
        print(path)
        # cv2.imshow('image',croped_img)
        # cv2.waitKey(0)
        client_id = init_remote_api_server()

        # Check if connected to Remote API server and maze array has been generated successfully
        if (client_id != -1):
                        # Send maze array data to CoppeliaSim via Remote API
                        return_code = send_data(maze_array)
                        path_vrep=vrep_path(path)
                        if (return_code == sim.simx_return_ok):
                            traverse_path(path_vrep)




if __name__=="__main__":
    main()