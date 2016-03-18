import os
import easygui
loc = ""
printing = []
tempparamloc = "F:\PS3\Other\Adventure Time Explore the Dungeon Because I DONT KNOW BLES01961\PS3_GAME\param.sfo"
##while 1:
##    if 
##        break
##    else:
##        continue
loc=easygui.diropenbox("Choose the folder that your backups are located in","Games Folder","F:\PS3")
if loc == "":
    loc = tempparamloc
'''
*slightly* modified code from Chris Krieger a.k.a LanThief
from http://lukasz.dk/mirror/forums.ps2dev.org/viewtopic60c6.html?t=923
'''
import sys 

def str2hex(s,size=8): 
    "String converter to hex" 
    if (len(s)*size) <= 32:    h = 0x0 
    else:                      h = 0x0L 
    for c in s: 
        h = (h << size) | ord(c) 
    return h 

def hex2hexList(h,size=8,reverse=True): 
    "hex converter to hex list" 
    return hex2hexList_charList(h,size,reverse,False) 

def hex2hexList_charList(h,size=8,reverse=True,ischr=True): 
    "hex converter to either chr list or hex list" 
    l = [] 
    if h == 0x0: 
        if ischr: l.append(chr(h)) 
        else: l.append(h) 
        return l 
    while h: 
        _h = (h & mask_bit(size)) 
        if ischr: horc = chr(_h) 
        else: horc = _h 
        l.append(horc) 
        h = (h >> size) 
    if reverse:l.reverse() 
    return l 

def str2hexList(s, size = 8, reverse=True): 
    "String converter to hex list" 
    return hex2hexList( str2hex(s), size, reverse ) 

def mask_bit(size=8): 
    if size > 32:   return (0x1L << size) - (0x1) 
    else:           return (0x1  << size) - (0x1) 
    
PsfMagic = "\0PSF" 
PsfDefaultFile = "PARAM.SFO" 

def le32(bits): 
    bytes = str2hexList(bits) 
    result = 0x0 
    offset = 0 
    for byte in bytes: 
        result |= byte << offset 
        offset +=8 
    return result 
##    # IndexError on zero bits - removed code 
##    return (bytes[0] | (bytes[1]<<8) | (bytes[2]<<16) | (bytes[3]<<24))  

def le16(bits): 
    bytes = str2hexList(bits) 
    if len(bytes) > 1: 
        return (bytes[0] | bytes[1]<<8) 
    return (bytes[0] | 0x0<<8) 

class PsfHdr: 
    size = 20 
    def __init__(self, bits): 
        self.size = 20 
        self.data = bits[:self.size] 
        self.magic = str2hexList( bits[:4] ) 
        self.rfu000 = str2hexList( bits[4:8] ) 
        self.label_ptr = bits[8:12] 
        self.data_ptr = bits[12:16] 
        self.nsects = bits[16:20] 

    def __len__(self): 
        return self.size 

class PsfSec: 
    size = 16 
    def __init__(self, bits): 
        self.size = 16 
        self.data = bits[:self.size] 
        self.label_off = bits[:2] 
        self.rfu001 = bits[2:3] 
        self.data_type = str2hex(bits[3:4]) # string=2, integer=4, binary=0 
        self.datafield_used = bits[4:8] 
        self.datafield_size = bits[8:12] 
        self.data_off = bits[12:16] 

    def __len__(self): 
        return self.size 
        
psf = None 

def chris(fileloc): 
    global psf
    PsfFilename = ( fileloc, PsfDefaultFile )[False]   # I use a slice [1:2] to avoid IndexError 
    PsfFile = open(PsfFilename,'rb')
    psf = PsfFile.read() 
    PsfFile.close()
    psfheader = PsfHdr(psf) 
    psfsections = PsfSec(psf[PsfHdr.size:]) 
    psflabels = psf[le32(psfheader.label_ptr):] 
    psfdata = psf[le32(psfheader.data_ptr):] 
    index = PsfHdr.size
    sect = psfsections
    wanted_details = {'PS3_SYSTEM_VER','TITLE','TITLE_ID'}
    templist = []
    for i in xrange(0, le32(psfheader.nsects) ):
        if psflabels[le16(sect.label_off):].split('\x00')[0] in wanted_details:
            print "%-18s = " %(psflabels[le16(sect.label_off):].split('\x00')[0]), 

            if sect.data_type   == 0x2:         # string
                if psflabels[le16(sect.label_off):].split('\x00')[0] == 'PS3_SYSTEM_VER':
                    if len(psfdata[le32(sect.data_off):].split('\x00\x00')[0][1:-4]) == 4:
                        print "%s" % psfdata[le32(sect.data_off):].split('\x00\x00')[0][1:-4]
                        templist.append(psfdata[le32(sect.data_off):].split('\x00\x00')[0][1:-4])
                    else:
                        continue
                else:
                    print "%s" % psfdata[le32(sect.data_off):].split('\x00\x00')[0]
                    templist.append(psfdata[le32(sect.data_off):].split('\x00\x00')[0])
                
            elif sect.data_type == 0x4:         # Integer 
                print "%d" % le32(psfdata[le32(sect.data_off)])
                templist.append(le32(psfdata[le32(sect.data_off)]))
                        
            elif sect.data_type == 0x0:         # binary data ? 
                print "Binary Data"

        index += PsfSec.size 
        sect = PsfSec(psf[index:])
    if len(templist) == 3:
        printing.append(templist[2]+"          "+templist[0]+"          "+templist[1])

'''
LanThief code ends here
'''

#loc = raw_input("Enter the location to look around. For now, just press enter")
#loc = "F:\PS3"
pkglist = []
pkgignore =["DATA000","DLC","nlock","addon","patch","-NP","-BL",]

for root, subdirs, files in os.walk(loc):
    littlelist=[]
    for fi in files:
        if ('.PKG' in fi or '.pkg' in fi) and 'PS3_GAME' not in root and len(fi)<45 and not any(substring in fi for substring in pkgignore):
            littlelist.append(fi)
    pkglist.extend(littlelist)
    if 'PARAM.SFO' in files and 'PS3_GAME' in root:
        chris(os.path.join(root,"PARAM.SFO"))
        continue

choice = easygui.choicebox("These are the backups that were found.","PS3 Library",printing)
choice = easygui.choicebox("These are PKG's that were found.","PS3 Library",pkglist)
    
print '\n\n\nYOU ALSO HAVE PKGs'
for x in pkglist:
    print x
