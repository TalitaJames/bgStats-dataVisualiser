from PIL import Image, ImageDraw, ImageFont 

width = 1080
height = 1920

#create the coloured overlays
colorOptions = {
    'dark_blue':(27,53,81),
    'grey':(70,86,95),
    'light_blue':(93,188,210),
    'blue':(23,114,237),
    'orange':(242,174,100),
    'purple':(114,88,136),
    'red':(255,0,0),
    'yellow':(255,255,0),
    'yellow_green':(232,240,165),
    'green':(65, 162, 77),
    'white':(255,255,255),
    'black':(0,0,0)
    
    }

imTest=Image.new('RGB', (width,height), color=colorOptions['white']) 



  
# create rectangle image
img1 = ImageDraw.Draw(imTest)  
img1.rectangle([(width/3,height/3),(2*width/3,2*height/3)], fill ="blue", outline ="red")

imTest.save('pictureExports/test.png')