

def delete_invalid(name):
    f = open(".//bib//"+name,'r')
    contents = []
    for line in f:
        line = line.replace("</td>","")
        line = line.replace("<td>","")
        line = line.replace("<tr>","")
        line = line.replace("</tr>","")
        contents.append(line)
    f.close()
    f = open(".//new//"+name,"w")
    for line in contents:
        f.write(line)
    f.flush()
    f.close()

if __name__ == "__main__":
    for i in range(1,67):
        name = str(i)
        if i<10:
            name = "0"+name
        delete_invalid(name)
    

