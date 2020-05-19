import argparse
import os
import os.path
import subprocess
import shutil
from distutils.dir_util import copy_tree
import time
import csv


class Smt_Stor(object):
    #---Define Class Variables
    data_path = '/ssd2/Registration_Datasets/'
    log_path = data_path + 'Timer_Log.csv'
    log_string = ''
    cam_call_1 = ' Camera'
    cam_call_2 = ' CameraType'
    cam_call_3 = ' Camera_Type'
    perm = 'echo nvidia | sudo -S -k '
    suffix = ''
    fields = ['Module', 'Flight', 'Band', '# of Images', 'Processing Time', 'Images/Second']
    

    def __init__(self,args):
        if not args.dir:
            print('no save path specified!')
        else:
            self.data_path = args.dir
        
        if not args.suf:
            print('no suffix specified')
        else:
            self.suffix = args.suf

        print('datapath = ' + self.data_path)

        if args.all:
            print('all is true!')

    
#---Define Class Methods------------------
        
    def logger(self, file_path, row):
        with open(file_path, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)
   
    def makeLogs(self, folder):
        print(folder)
        if not os.path.exists(self.data_path + folder + '/.data'):
            os.mkdir(self.data_path + folder + '/.data')
        if not os.path.exists(self.data_path + folder + '/.data/QuickTile.log'):
            open(self.data_path + folder + '/.data/QuickTile.log', 'a')
                        
        if not os.path.exists(self.data_path + folder + '/.data'):
            os.mkdir(self.data_path + folder + '/.data')
        if not os.path.exists(self.data_path + folder + '/.data/QuickMoaic.log'):
            open(self.data_path + folder + '/.data/QuickMosaic.log', 'a')

        if not os.path.exists(self.data_path + folder + '/.data'):
            os.mkdir(self.data_path + folder + '/.data')
        if not os.path.exists(self.data_path + folder + '/.data/Snap.log'):
            open(self.data_path + folder + '/.data/Snap.log', 'a')

    def getQTLog(self, data):
        return ' > ' + self.data_path + data + '/.data/QuickTile.log'

    def getQMLog(self, data):
        return ' > ' + self.data_path + data + '/.data/QuickMosaic.log'

    def getSnapLog(self, data):
        return ' > ' + self.data_path + data + '/.data/Snap.log'

    def getVersion(self, module):
        cmd = '/var/SmartStorage/bin/' + module + ' --version'
        output = subprocess.Popen([cmd], shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        stdout, stderr = output.communicate()
        versionNumDirty = str(stdout)
        versionNumUgly = versionNumDirty.replace('.', '_')
        versionNum = versionNumUgly.rstrip()
        return versionNum

    def renameFiles(self, folder, module, suffix):
        listOfFiles = os.listdir(folder)
        versionNumber = self.getVersion(module)
        print(listOfFiles)
        for fileNames in listOfFiles:
            meatOfFile = fileNames.rpartition('.')
            os.rename(folder + '/' + fileNames, folder + '/' + meatOfFile[0] + versionNumber + suffix + '_' + self.suffix + meatOfFile[-2] + meatOfFile[-1])

    def RunQuickTile(self, Dataset):
        print("------------------------------------------------------------------------------------Calling QuickTile on all folders in " + Dataset)
        cmd = store.perm + '/var/SmartStorage/bin/QuickTile' + ' ' + self.data_path + Dataset + '/' + self.getQTLog(Dataset)
        subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
    def RunQuickMosaic(self, Dataset):
        if os.path.exists(self.data_path + Dataset + '/LWIR_FullRes'):
            Dir = self.data_path + Dataset + '/LWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on LWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            Dir = self.data_path + Dataset + '/LWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on LWIR with color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight true' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)          


        if os.path.exists(self.data_path + Dataset + '/MWIR_FullRes'):
            Dir = self.data_path + Dataset + '/MWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on MWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            Dir = self.data_path + Dataset + '/MWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on MWIR with color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight true' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)
        

        if os.path.exists(self.data_path + Dataset + '/SWIR_FullRes'):
            Dir = self.data_path + Dataset + '/SWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on SWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' SWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            
        if os.path.exists(self.data_path + Dataset + '/RGB_FullRes'):
            Dir = self.data_path + Dataset + '/RGB_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])   
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on RGB with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' RGB Hotspot_Highlight false' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)
        

        if os.path.exists(self.data_path + Dataset + '/NIR_FullRes'):
            Dir = self.data_path + Dataset + '/NIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on NIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' NIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['QuickMosaic', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)


    def RunSuperOverlay(self, Dataset):
        if os.path.exists(self.data_path + Dataset + '/LWIR_FullRes'):
            Dir = self.data_path + Dataset + '/LWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling SuperOverlay on LWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight false Output_Type SuperOverlay' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            if args.qmcolor or args.all:
                Dir = self.data_path + Dataset + '/LWIR_FullRes'
                imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
                print('--------------------------------------------------------------------------------------Calling SuperOverlay on LWIR with color')
                cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight true Output_Type SuperOverlay' + self.getQMLog(Dataset)
                timeA = time.time()
                subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
                timeB = time.time()
                timeZ = timeB - timeA
                self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
                self.logger(store.log_path, store.log_string)          


        if os.path.exists(self.data_path + Dataset + '/MWIR_FullRes'):
            Dir = self.data_path + Dataset + '/MWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling SuperOverlay on MWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight false Output_Type SuperOverlay' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            if args.qmcolor or args.all:
                Dir = self.data_path + Dataset + '/MWIR_FullRes'
                imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
                print('--------------------------------------------------------------------------------------Calling SuperOverlay on MWIR with color')
                cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight true Output_Type SuperOverlay' + self.getQMLog(Dataset)
                timeA = time.time()
                subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
                timeB = time.time()
                timeZ = timeB - timeA
                self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
                self.logger(store.log_path, store.log_string)
            

        if os.path.exists(self.data_path + Dataset + '/SWIR_FullRes'):
            Dir = self.data_path + Dataset + '/SWIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling SuperOverlay on SWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' SWIR Hotspot_Highlight false Output_Type SuperOverlay' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

            
        if os.path.exists(self.data_path + Dataset + '/RGB_FullRes'):
            Dir = self.data_path + Dataset + '/RGB_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])   
            print('--------------------------------------------------------------------------------------Calling SuperOverlay on RGB with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' RGB Hotspot_Highlight false Output_Type SuperOverlay' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)
        

        if os.path.exists(self.data_path + Dataset + '/NIR_FullRes'):
            Dir = self.data_path + Dataset + '/NIR_FullRes'
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling SuperOverlay on NIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' NIR Hotspot_Highlight false Output_Type SuperOverlay' + self.getQMLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['SuperOverlay', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)


    def RunSnap(self, Dataset):

        Dir = self.data_path + Dataset + '/LWIR_FullRes'
        if os.path.exists(Dir):
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            cmd = ' rm -rf ' + Dir + '/*snapped*.csv '
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)

            print('--------------------------------------------------------------------------------------Calling Snap on LWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' LWIR' + self.getSnapLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['Snap', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

        Dir = self.data_path + Dataset + '/MWIR_FullRes'
        if os.path.exists(Dir):
            cmd = ' rm -rf ' + Dir + '/*snapped*.csv '
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling Snap on MWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' MWIR' + self.getSnapLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['Snap', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)
        
        Dir = self.data_path + Dataset + '/SWIR_FullRes'
        if os.path.exists(Dir):
            cmd = ' rm -rf ' + Dir + '/*snapped*.csv '
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)    

            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling Snap on SWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' SWIR' + self.getSnapLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['Snap', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

        Dir = self.data_path + Dataset + '/RGB_FullRes'
        if os.path.exists(Dir):
            cmd = ' rm -rf ' + Dir + '/*snapped*.csv '
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT) 
            
            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling Snap on RGB')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + self.data_path + Dataset + store.cam_call_2 +' RGB' + self.getSnapLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['Snap', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

        Dir = self.data_path + Dataset + '/NIR_FullRes'   
        if os.path.exists(self.data_path + Dataset + '/NIR_FullRes'):
            cmd = ' rm -rf ' + Dir + '/*snapped*.csv '
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)

            imgNum = len([name for name in os.listdir(Dir) if os.path.isfile(os.path.join(Dir, name))])
            print('--------------------------------------------------------------------------------------Calling Snap on NIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + self.data_path + Dataset + store.cam_call_2 + ' NIR' + self.getSnapLog(Dataset)
            timeA = time.time()
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            timeB = time.time()
            timeZ = timeB - timeA
            self.log_string = ['Snap', Dataset, Dir[-12:-8], imgNum, int(timeZ), int(imgNum/timeZ)]
            self.logger(store.log_path, store.log_string)

    def DeleteContents(self, path):
        if os.path.exists(path):
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
            else:
                items = os.listdir(path)
                for item in items:
                    os.remove(path + '/' + item)

def parse_cmd_line():
    # Parse the command line for the arguments
    parser = argparse.ArgumentParser(description='runs smart storage modules on folder specified')
    parser.add_argument("--quickmosaic", help="runs quickmosaic", action="store_true")
    parser.add_argument("--qmcolor", help="runs quickmosaic with color", action="store_true")
    parser.add_argument("--snap", help="runs snap", action="store_true")
    parser.add_argument("--quicktile", help="runs quicktile", action="store_true")
    parser.add_argument("--all", help="runs all modules", action="store_true")
    parser.add_argument('--dir', help="path to load flights to process", type=str)
    parser.add_argument('--suf', help="path to load flights to process", type=str)
    
    return parser.parse_args()

args = parse_cmd_line()

if not args.all:
    print('not all!')
    all = True
else:
    print('all!!')


store = Smt_Stor(args)

dataPath = store.data_path[:-1]

Test_Dataset = os.listdir(dataPath) #list and location of Fligt number
print("Flight folders being processed are:")
print(Test_Dataset)

store.logger(store.log_path, store.fields) #run the logger with fields to help indicate to the user where the most recent test was run


for Dataset in Test_Dataset:
    #---------------LOGS---------
    print(Dataset)
    store.makeLogs(Dataset)
    if not store.suffix:
        results_data_path = store.data_path + 'Results'
    else:
        results_data_path = store.data_path + 'Results_' + store.suffix

    if os.path.exists(results_data_path):
        print(results_data_path + ' already exists.')
    else :
        os.mkdir(results_data_path)
    
    if args.quicktile or args.all:
        #---------------QUICKTILE-PRE-SNAP---------
        store.RunQuickTile(Dataset)
        from_Directory = store.data_path + Dataset + '/QuickTile/'
        dest_Directory = results_data_path + '/' + Dataset + '/QuickTile_PreSnap' + store.getVersion('QuickTile')
        copy_tree(from_Directory, dest_Directory)
        shutil.rmtree(from_Directory)
        
        store.renameFiles(dest_Directory, 'QuickTile', 'preSnap')
        data_folder = store.data_path + Dataset + '/.data/' 
        new_data_folder = results_data_path + '/' + Dataset + '/QuickTile_PreSnap_DATA_' + store.getVersion('QuickTile')
        copy_tree(data_folder, new_data_folder)
        


    #-------------QUICKMOSAIC-PRE-SNAP----------
    store.RunQuickMosaic(Dataset)
    #Clean up folder
    from_Directory = store.data_path + Dataset + '/QuickMosaic/'
    dest_Directory = results_data_path + '/' + Dataset + '/QuickMosaic_PreSnap_' + store.getVersion('QuickMosaic')
    copy_tree(from_Directory, dest_Directory)
    store.renameFiles(dest_Directory, 'QuickMosaic', store.suffix)
    data_folder = store.data_path + Dataset + '/.data/'
    new_data_folder = results_data_path + '/' + Dataset + '/QuickMosaic_PreSnap_DATA_' + store.getVersion('QuickMosaic')
    copy_tree(data_folder, new_data_folder)
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #-------------SUPEROVERLAY-PRE-SNAP----------
    store.RunSuperOverlay(Dataset)
    #Clean up folder
    from_Directory = store.data_path + Dataset + '/Superoverlays/'
    dest_Directory = results_data_path + '/' + Dataset + '/SuperOverlays_PreSnap_' + store.getVersion('QuickMosaic')
    copy_tree(from_Directory, dest_Directory)
    store.renameFiles(dest_Directory, 'QuickMosaic', store.suffix)
    data_folder = store.data_path + Dataset + '/.data/'
    new_data_folder = results_data_path + '/' + Dataset + '/SuperOverlays_PreSnap_DATA_' + store.getVersion('QuickMosaic')
    copy_tree(data_folder, new_data_folder)
    store.DeleteContents(data_folder)
    #store.DeleteContents(from_Directory) This errored out becasue the directory is not empty and my DeleteContents method did not clean the folders as expected
    shutil.rmtree(from_Directory)


    data_folder = store.data_path + Dataset + '/.data' 
    store.RunSnap(Dataset)
    new_data_folder = results_data_path + '/' + Dataset + '/Snap_DATA_' + store.getVersion('Snap')
    #------------------SNAP-----------------------
    if os.path.exists(new_data_folder):
        print(new_data_folder + ' already exists.')
    else :
        os.mkdir(new_data_folder)

    copy_tree(data_folder, new_data_folder)
    store.DeleteContents(data_folder)


    #----------------QUICKTILE-POST-SNAP------------------
    store.RunQuickTile(Dataset)
    #Clean up folder
    from_Directory = store.data_path + Dataset + '/QuickTile/'
    dest_Directory = results_data_path + '/' + Dataset + '/QuickTile_PostSnap' + store.getVersion('QuickTile')
    copy_tree(from_Directory, dest_Directory)
    store.renameFiles(dest_Directory, 'QuickTile', store.suffix)
    data_folder = store.data_path + Dataset + '/.data/' 
    new_data_folder = results_data_path + '/' + Dataset + '/QuickTile_PostSnap_DATA_' + store.getVersion('QuickTile')
    copy_tree(data_folder, new_data_folder)
    #store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #-------------------QUICKMOSAIC-POST-SNAP----------------------
    store.RunQuickMosaic(Dataset)
    #Clean up folder
    from_Directory = store.data_path + Dataset + '/QuickMosaic/'
    dest_Directory = results_data_path + '/' + Dataset + '/QuickMosaic_PostSnap_' + store.getVersion('QuickMosaic')
    copy_tree(from_Directory, dest_Directory)
    store.renameFiles(dest_Directory, 'QuickMosaic', store.suffix)
    data_folder = store.data_path + Dataset + '/.data/' 
    data_folder = store.data_path + Dataset + '/.data/'
    new_data_folder = results_data_path + '/' + Dataset + '/QuickMosaic_PostSnap_DATA_' + store.getVersion('QuickMosaic')
    copy_tree(data_folder, new_data_folder)
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)

    if args.snap and args.quickmosaic or args.all:
        #-------------SUPEROVERLAY-POST-SNAP----------
        store.RunSuperOverlay(Dataset)
        #Clean up folder
        from_Directory = store.data_path + Dataset + '/Superoverlays/'
        dest_Directory = results_data_path + '/' + Dataset + '/SuperOverlays_PostSnap_' + store.getVersion('QuickMosaic')
        copy_tree(from_Directory, dest_Directory)
        shutil.rmtree(from_Directory)

        store.renameFiles(dest_Directory, 'QuickMosaic','post_snap')

        data_folder = store.data_path + Dataset + '/.data/'
        new_data_folder = results_data_path + '/' + Dataset + '/SuperOverlays_PostSnap_DATA_' + store.getVersion('QuickMosaic')
        copy_tree(data_folder, new_data_folder)
        shutil.rmtree(data_folder)
        

print('Automated Testing Completed')
