import json, sys, cv2
import multiprocessing
json_path = sys.argv[1]

boxs_all = {}

with open(json_path) as f:
  data = json.load(f)
  for key in data:
      print(data[key].keys())
      

      print("filename:", data[key]['filename'])
      filename = data[key]['filename']
      print("size:", data[key]['size'])
      print( "regions:", data[key]['regions'])
      print("file attributes:", data[key]['file_attributes'])
      box_dict = {}
      regions = data[key]['regions']
      for region in regions:
          print(region['shape_attributes'].keys())
          x_points = region['shape_attributes']['all_points_x']
          y_points = region['shape_attributes']['all_points_y']
          bbox = [min(x_points), min(y_points), max(x_points), max(y_points)]
          name = region['region_attributes']['name']
          if name not in box_dict:
              box_dict[name] = [bbox]
          else:
              box_dict[name] += [bbox]

      boxs_all[filename] = box_dict


def readBoxes(fname, new_path, width, height):

    labelledObjects = boxs_all[fname]
    newxml = write_xml(fname, labelledObjects, width, height)
    g = open(new_path,'w')
    g.write(newxml)
    g.close()



def write_xml(file_name, objects, width, height):
    ann = "<annotation><folder>DAMAGE</folder><filename>"+file_name+"</filename><segmented>0</segmented><source><database>DAMAGE-DB</database><annotation>DAMAGE-DB</annotation><image>DAMAGE-DB</image><flickrid>damage</flickrid></source><owner><flickrid>fgvc</flickrid><name>fgvc</name></owner>"
    ann += "<size><width>"+str(width)+"</width><height>"+str( height)+"</height><depth>3</depth></size>"
    for obj in objects:
      for ins in objects[obj]:
          ann += "<object><name>"+obj+"</name><pose>frontal</pose><truncated>0</truncated><difficult>0</difficult><bndbox><xmin>"+str(ins[0])+"</xmin><ymin>"+str(ins[1])+"</ymin><xmax>"+str(ins[2])+"</xmax><ymax>"+str(ins[3])+"</ymax></bndbox></object>"
    ann += "</annotation>"
    return ann

import os, shutil

def files_with_ext(mypath, ext):
    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and os.path.splitext(os.path.join(mypath, f))[1] == ext]
    return files


if __name__ == '__main__':
    mypath = sys.argv[2]
    outputpath = sys.argv[3]
    if not os.path.exists(outputpath):
       os.makedirs(outputpath)

    images = files_with_ext(mypath, '.jpg')
#    images = [os.path.join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    #images = open('images_box.txt','r').readlines()
    count  = 0
    totalCount = 0
    jobs = []
    for image in images:
        print(image)
        name = os.path.join(mypath, image.strip())
        print(name)
        I = cv2.imread(image)
        width, height = I.shape[:-1]
        p = multiprocessing.Process(target=readBoxes, args=(os.path.basename(name), os.path.join(outputpath, os.path.basename(image).replace('.jpg','') +'.xml'), width, height, ))
        jobs.append(p)
        totalCount = totalCount + 1
        p.start()


      



     



