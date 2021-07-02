maze_array = {}
baseHandle = -1      
textureID = -1        
textureData = -1 



function createWall()
      
    wallObjectHandle = sim.createPureShape(0, 26, {0.35, 0.01, 0.1}, 0, nil)   
    sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_measurable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_detectable_all)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_renderable)
    return wallObjectHandle
end

function saveTexture()
    baseHandle = sim.getObjectHandle("Base")
    textureID = sim.getShapeTextureId(baseHandle)
    textureData=sim.readTexture(textureID ,0,0,0,0,0)
    sim.saveImage(textureData, {512,512}, 0, "models/other/base_template.png", -1)
end

function retrieveTexture()
    textureData, resolution = sim.loadImage(0, "models/other/base_template.png") 
end

function reapplyTexture()
    plane, textureID = sim.createTexture("", 0, nil, {1.01, 1.01}, nil, 0, {512, 512})
    sim.writeTexture(textureID, 0, textureData, 0, 0, 0, 0, 0)
    sim.setShapeTexture(baseHandle, textureID, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil)
    sim.removeObject(plane)
end

function receiveData(inInts,inFloats,inStrings,inBuffer)


    maze_array=inInts
    --print(maze_array[1])
    
    return inInts, inFloats, inStrings, inBuffer
end

function generateHorizontalWalls()

    
    boh=sim.getObjectHandle('Base')
    wallObjectHandleh={}
    y=1.8
    for i=1,11,1
    do
    x=-1.63
    wallObjectHandleh[i]={}
    
        for j=1,10,1
        do
            wallObjectHandleh[i][j] = createWall()
            sim.setObjectParent(wallObjectHandleh[i][j],boh,True)
            sim.setObjectPosition(wallObjectHandleh[i][j],boh,{x,y,0.065})
            x=x+0.36
        end
        y=y-0.36
    end
    
    


end

function generateVerticalWalls()


    boh=sim.getObjectHandle('Base')
    wallObjectHandlev={}
    y=1.63
    for i=1,10,1
    do
    x=-1.8
    wallObjectHandlev[i]={}
    
        for j=1,11,1
        do
            wallObjectHandlev[i][j] = createWall()
            sim.setObjectOrientation(wallObjectHandlev[i][j],-1,{0,0,1.57})
            sim.setObjectParent(wallObjectHandlev[i][j],boh,True)
            sim.setObjectPosition(wallObjectHandlev[i][j],boh,{x,y,0.065})
            x=x+0.36
        end
        y=y-0.36
    end    
    

end


function createMaze(a)

    
    print('success')
    print(a[7])
    --horizontalwall()
    --verticalwall()
    arr=1
    ih=2
    jh=1
    iv=1
    jv=2

    for k=1,100,1 do
        --remove r,b
        if(a[arr]<4) then
            sim.removeObject(wallObjectHandleh[ih][jh])
            wallObjectHandleh[ih][jh]=-5
            sim.removeObject(wallObjectHandlev[iv][jv])
            wallObjectHandlev[iv][jv]=-5
        end
        --remove b
        if(a[arr]>3 and a[arr]<8) then
            sim.removeObject(wallObjectHandleh[ih][jh])
            wallObjectHandleh[ih][jh]=-5
        end
        --remove r
        if(a[arr]>7 and a[arr]<12) then
            sim.removeObject(wallObjectHandlev[iv][jv])
            wallObjectHandlev[iv][jv]=-5
        end
        if(k%10==0) then
            ih=ih+1
            iv=iv+1
            jh=0
            jv=1
        end
        jh=jh+1
        jv=jv+1
        arr=arr+1
    end    
    
end



function deleteWalls()

    
    for i=1,11,1
    do
        for j=1,10,1
        do
            if(wallObjectHandleh[i][j]~=-5) then
                sim.removeObject(wallObjectHandleh[i][j])
            end
        end
    end  
    for i=1,10,1
    do
        for j=1,11,1
        do
            if(wallObjectHandlev[i][j]~=-5) then
                sim.removeObject(wallObjectHandlev[i][j])
            end
        end
    end


end



function sysCall_init()

    if pcall(saveTexture) then 
        print("Successfully saved texture")
    else
        print("Texture does not exist. Importing texture from file..")
        retrieveTexture()
        reapplyTexture()
    end 
  
end

function sysCall_nonSimulation()
    -- is executed when simulation is not running
end

function sysCall_beforeSimulation()
    -- is executed before a simulation starts
    sim.setShapeTexture(baseHandle, -1, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil) -- Do not delete or modify this line
    h=1
    generateHorizontalWalls()
    generateVerticalWalls()
    createMaze(maze_array)
end

function sysCall_afterSimulation()
    -- is executed before a simulation ends
    deleteWalls()
    reapplyTexture()
end

function sysCall_cleanup()
    -- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details
