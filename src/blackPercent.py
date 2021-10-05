from PIL import Image

def bpercent(im): 
    # im = Image.open('sw1.jpg')
    pixels = im.getdata()
    black_thresh = 20
    nblack = 0
    for pixel in pixels:
        if (pixel[0] < black_thresh)and(pixel[1] < black_thresh)and(pixel[2] < black_thresh):
            nblack += 1
    n = len(pixels)
    
    perc = nblack / float(n)
    print(perc)
    if (perc > 0.8): return False
    else : return True
    

    