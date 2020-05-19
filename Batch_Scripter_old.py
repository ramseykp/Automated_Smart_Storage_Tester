import os
import subprocess
import shutil
from distutils.dir_util import copy_tree

class Smt_Stor():
#---Define Class Variables
    log_path = '/ssd2/Registration_Datasets/Smt_Stor_log.txt'
    log_string = ''
    cam_call_1 = ' Camera'
    cam_call_2 = ' CameraType'
    cam_call_3 = ' Camera_Type'
    perm = 'echo nvidia | sudo -S -k '
    
    
#---Define Class Methods------------------
    def logger(self, file_path, log_string):
        with open(file_path, 'a') as f:
            f.write(log_string + '\n')
   
    def makeLogs(self, folder):
        print(folder)
        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data'):
            os.mkdir('/ssd2/Registration_Datasets/' + folder + '/.data')
        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data/QuickTile.log'):
            open('/ssd2/Registration_Datasets/' + folder + '/.data/QuickTile.log', 'a')
                        
        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data'):
            os.mkdir('/ssd2/Registration_Datasets/' + folder + '/.data')
        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data/QuickMoaic.log'):
            open('/ssd2/Registration_Datasets/' + folder + '/.data/QuickMosaic.log', 'a')

        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data'):
            os.mkdir('/ssd2/Registration_Datasets/' + folder + '/.data')
        if not os.path.exists('/ssd2/Registration_Datasets/' + folder + '/.data/Snap.log'):
            open('/ssd2/Registration_Datasets/' + folder + '/.data/Snap.log', 'a')

    def getQTLog(self, data):
        return ' > /ssd2/Registration_Datasets/' + data + '/.data/QuickTile.log'

    def getQMLog(self, data):
        return ' > /ssd2/Registration_Datasets/' + data + '/.data/QuickMosaic.log'

    def getSnapLog(self, data):
        return ' > /ssd2/Registration_Datasets/' + data + '/.data/Snap.log'

    def getVersion(self, module):
        cmd = '/var/SmartStorage/bin/' + module + ' --version'
        output = subprocess.Popen([cmd], shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        stdout, stderr = output.communicate()
        versionNumDirty = str(stdout)
        versParts = versionNumDirty.rpartition('.')
        versParts[0] = versParts[0].replace('.', '_')
        versionNum = versParts[0] + versParts[1] + versParts[2]
        return versionNum

    def renameFiles(self, folder, module):
        listOfFiles = os.listdir(folder)
        versionNumber = self.getVersion(module)
        print(listOfFiles)
        for fileNames in listOfFiles:
            meatOfFile = fileNames.rpartition('.')
            print(meatOfFile[0])
            print(meatOfFile[-2])
            print(meatOfFile[-1])
            os.rename(folder + '/' + fileNames, folder + '/' + meatOfFile[0] + versionNumber + meatOfFile[-2] + meatOfFile[-1])

    def RunQuickTile(self, Dataset):
        print("------------------------------------------------------------------------------------Calling QuickTile on all folders in " + Dataset)
        cmd = store.perm + '/var/SmartStorage/bin/QuickTile' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + '/' + self.getQTLog(Dataset)
        subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
    def RunQuickMosaic(self, Dataset):
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/LWIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on LWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT) 
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on LWIR with color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' LWIR Hotspot_Highlight true' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/MWIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on MWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on MWIR with color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' MWIR Hotspot_Highlight true' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/SWIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on SWIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' SWIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/RGB_FullRes'):    
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on RGB with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' RGB Hotspot_Highlight false' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/NIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling QuickMosaic on NIR with no color')
            cmd = store.perm + '/var/SmartStorage/bin/QuickMosaic' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' NIR Hotspot_Highlight false' + self.getQMLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)

    def RunSnap(self, Dataset):
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/LWIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling Snap on LWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' LWIR' + self.getSnapLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/MWIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling Snap on MWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' MWIR' + self.getSnapLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/SWIR_FullRes'):    
            print('--------------------------------------------------------------------------------------Calling Snap on SWIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' SWIR' + self.getSnapLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
        
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/RGB_FullRes'):
            print('--------------------------------------------------------------------------------------Calling Snap on RGB')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 +' RGB' + self.getSnapLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
            
        if os.path.exists('/ssd2/Registration_Datasets/' + Dataset + '/NIR_FullRes'):
            print('--------------------------------------------------------------------------------------Calling Snap on NIR')
            cmd = store.perm + '/var/SmartStorage/bin/Snap' + ' ' + '/ssd2/Registration_Datasets/' + Dataset + store.cam_call_2 + ' NIR' + self.getSnapLog(Dataset)
            subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)

    def DeleteContents(self, path):
        if os.path.exists(path):
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
            else:
                items = os.listdir(path)
                for item in items:
                    os.remove(path + '/' + item)
                #os.rmdir(path) #my original attempt at removing the folder
                #cmd = echo "nvidia" | sudo -S rm -rf .data
                #subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)
 
    #def VersionChecker(self, module):
     #   cmd = 'var/SmartStorage/bin/' module ' --version'
      #  subprocess.check_call([cmd], shell = True, stderr = subprocess.STDOUT)

Test_Dataset = os.listdir('/ssd2/Registration_Datasets') #list and location of Fligt number
print(Test_Dataset)

store = Smt_Stor()
#I think these belong within the Class
#Test_Dataset = os.listdir('/ssd2/Registration_Datasets') #list and location of Fligt number
#print(Test_Dataset)
#commented out here
for Dataset in Test_Dataset:
    #---------------QUICK_TILE_PRESNAP---------
    print(Dataset)
    store.makeLogs(Dataset)
    store.log_string = 'Starting QuickTile presnap'
    store.logger(store.log_path, store.log_string)
    store.RunQuickTile(Dataset)
    store.log_string = 'Finished QuickTile'
    store.logger(store.log_path, store.log_string)


    from_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickTile/'
    dest_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickTile_PreSnap_' + store.getVersion('QuickTile')
    copy_tree(from_Directory, dest_Directory)
    store.renameFiles(dest_Directory, QuickTile)
    data_folder = '/ssd2/Registration_Datasets/' + Dataset + '/.data/'
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #-------------QUICKMOSAIC----------
    store.log_string = 'Starting QuickMosaic presnap'
    store.logger(store.log_path, store.log_string)
    store.RunQuickMosaic(Dataset)
    store.log_string = 'Finished QuickMosaic'
    store.logger(store.log_path, store.log_string)
    
    from_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickMosaic/'
    dest_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickMosaic_PreSnap_' + store.getVersion('QuickMosaic')
    copy_tree(from_Directory, dest_Directory)
    data_folder = '/ssd2/Registration_Datasets/' + Dataset + '/.data/'
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #------------------SNAP-----------------------
    store.log_string = 'Starting SNAP'
    store.logger(store.log_path, store.log_string)
    store.RunSnap(Dataset)
    store.log_string = 'Finished SNAP'
    store.logger(store.log_path, store.log_string)

    data_folder = '/ssd2/Registration_Datasets/' + Dataset + '/.data/' 
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #----------------QUICKTILE-POST-SNAP------------------
    store.log_string = 'Starting QuickTile postsnap'
    store.logger(store.log_path, store.log_string)
    store.RunQuickTile(Dataset)
    store.log_string = 'Finished QuickTile'
    store.logger(store.log_path, store.log_string)
    
    from_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickTile/'
    dest_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickTile_PostSnap' + store.getVersion('QuickTile')
    copy_tree(from_Directory, dest_Directory)
    data_folder = '/ssd2/Registration_Datasets/' + Dataset + '/.data/' 
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)


    #-------------------QUICKMOSAIC-POST-SNAP----------------------
    store.log_string = 'Starting QuickMosaic postsnap'
    store.logger(store.log_path, store.log_string)
    store.RunQuickMosaic(Dataset)
    store.log_string = 'Finished QuickMosaic'
    store.logger(store.log_path, store.log_string)

    from_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickMosaic/'
    dest_Directory = '/ssd2/Registration_Datasets/' + Dataset + '/QuickMosaic_PostSnap_' + store.getVersion('QuickMosaic')
    copy_tree(from_Directory, dest_Directory)
    data_folder = '/ssd2/Registration_Datasets/' + Dataset + '/.data/' 
    store.DeleteContents(data_folder)
    store.DeleteContents(from_Directory)

print('Automated Testing Completed')
