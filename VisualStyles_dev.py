#Author - pawelzwronek(aka blowman3)
#Description - Quick change visuals style of active viewport
#Modified source of Show Hidden by Patrick Rainsberry

#Changelog
# v1.0 - Initial version
# v1.0.1 - Hiding buttons in 'COMPARE' workspace
# v1.2 - Customization and saving preferences to local disk and on cloud
# v1.2.1 - Move local configuration to roaming directory


import adsk.core, adsk.fusion, traceback
import os, datetime

# global event handlers referenced for the duration of the command
handlers = []

menu_panel = 'InspectPanel'
commandResources = './resources'

commandId = 'visualStyles'
commandName = 'Visual Styles'
commandDescription = 'Quick change visual style of active viewport'

S_CmdId = 'S_CmdId'
SHE_CmdId = 'SHE_CmdId'
SVEO_CmdId = 'SVEO_CmdId'
W_CmdId = 'W_CmdId'
WHE_CmdId = 'WHE_CmdId'
WVEO_CmdId = 'WVEO_CmdId'
visualStylesCmdCount = 6

VSS_CmdId = 'ViewVisualStyleSetup_CmdId'
LP_CmdId = 'LocalPreferences_CmdId'

# Defines order in "Visual Styles Setup" list
cmdIds = [S_CmdId, SHE_CmdId, SVEO_CmdId, W_CmdId, WHE_CmdId, WVEO_CmdId, LP_CmdId,
          VSS_CmdId]

localPreferencesLocation = visualStylesCmdCount

class Cmd:
    def __init__(self, id, name, res, vs=None):
        self.id = id
        self.name = name
        self.res = res
        self.vs = vs
        
vs = adsk.core.VisualStyles
cmds = {  S_CmdId : Cmd(S_CmdId,'Shaded', '/S', vs.ShadedVisualStyle),
          SHE_CmdId : Cmd(SHE_CmdId,'Shaded with Hidden Edges', '/SHE', vs.ShadedWithHiddenEdgesVisualStyle),
          SVEO_CmdId : Cmd(SVEO_CmdId, 'Shaded with Visible Edges Only', '/SVEO', vs.ShadedWithVisibleEdgesOnlyVisualStyle),
          W_CmdId : Cmd(W_CmdId,'Wireframe', '/W', vs.WireframeVisualStyle),
          WHE_CmdId : Cmd(WHE_CmdId, 'Wireframe with Hidden Edges', '/WHE', vs.WireframeWithHiddenEdgesVisualStyle),
          WVEO_CmdId : Cmd(WVEO_CmdId, 'Wireframe with Visible Edges Only', '/WVEO', vs.WireframeWithVisibleEdgesOnlyVisualStyle),
          VSS_CmdId : Cmd(VSS_CmdId, 'Visual Style Setup', None, None),
          LP_CmdId : Cmd(LP_CmdId, 'Local preferences (faster startup)', None, None)
    }

hideAll = False        
config = None
configFile = None
dontAskAgain = False
folder =None
progressDialog =None

logToFile =False
clicksInARow =0

def progress(msg, val=None):
    global progressDialog
    if progressDialog:
        if progressDialog.wasCancelled:
            adsk.doEvents()
            return True
        if msg:
            progressDialog.message = msg
            if val:
                progressDialog.progressValue = val
        else:
            progressDialog.hide()
            progressDialog =None
    elif msg:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = 'Cancel'
        progressDialog.isBackgroundTranslucent = True
        progressDialog.isCancelButtonShown = True
        progressDialog.show('Preferences configuration', msg,0,100)
        
    adsk.doEvents()
    return False


prjName = '_Preferences'
folderName = 'VisualStyles'
fileName = 'prefs'
configPath = os.path.join(os.environ['APPDATA'], 'Autodesk\\ApplicationPlugins\\')
localFileName = os.path.join(configPath, 'visualStylesPref.cfg')
localFileNameOffline = os.path.join(configPath, 'visualStylesPrefOffline.cfg')
def getPrefFile(forceLocal=False):
    print('getPrefFile()...')  

    app = adsk.core.Application.get()
    ui  = app.userInterface


    if forceLocal:
        return localFileName

    if os.path.exists(localFileName):
        print(localFileName + ' exists')
        return localFileName
    else:
        print(localFileName + ' not exists')
    
    
    global dontAskAgain
    if dontAskAgain:
        print('dontAskAgain=True returning None')
        return None
    
    print('Looking for project '+prjName)    
    prjExists = False
    prj =None
    for p in app.data.dataHubs.item(0).dataProjects:
        if p.name == prjName:
            print('Found project '+prjName)    
            prj = p
            prjExists = True
            break
    
    if prj is None:
        print('Not found project '+prjName)    
        ret = ui.messageBox('VisualStyles cloud preferences not created\n\n'
                        '    Press \'Yes\' to create project named  \'' + prjName + '\'\n'+
                        '    Inside appears folder  \''+folderName+'\'  with file named  \''+fileName+'\'\n\n'+
                        '    Press \'No\' to create local(this computer) preferences file\n\n'+
                        '    Press \'Cancel\' to ask againt later\n\n\n' 
                        '                               Tip: Setup is below \'Visual Style\' dropdown menu',
                        'VisualStyles preferences',
                        adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType)
        if ret==adsk.core.DialogResults.DialogYes:
            print('Creating project... '+prjName)
            #ui.messageBox('Creating project take some time. Press OK and wait a moment')
            progress('VisualStyles preferences configuration...')
            prj = app.data.dataHubs.item(0).dataProjects.add(prjName)
            progress('Creating project \''+prjName+'\'...', 30)
            print('... '+prjName)    
        elif ret==adsk.core.DialogResults.DialogNo:
            return localFileName
        elif ret==adsk.core.DialogResults.DialogCancel:
            dontAskAgain = True
            return localFileNameOffline

    if not prjExists:
        print('Looking for project '+prjName)    
        prj =None
        for p in app.data.dataHubs.item(0).dataProjects:
            if p.name == prjName:
                print('Found project '+prjName)    
                prj = p
                break
        if not prj:
            print('Failed creating project '+prjName)    
            ui.messageBox('Unable to create project  \'' +prjName+ '\'  :(\n'
                            'Try again later or please create it manualy')
            return localFileNameOffline

    print('Looking for folder '+folderName)    
    folder = prj.rootFolder.dataFolders.itemByName(folderName)
    if not folder:
        print('Folder not found '+folderName)    
        ret =None
        if prjExists:
            ret = ui.messageBox('VisualStyles folder not created in preferences project\n\n'
                            '    Press \'Yes\' to create it \n'+
                            '    Press \'No\' to create local(this computer) preferences file\n\n'+
                            '    Press \'Cancel\' to ask againt later\n' ,
                            '    VisualStyles preferences',
                            adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType)
        
        if not prjExists or ret==adsk.core.DialogResults.DialogYes:
            print('Creating folder... '+folderName)    
            progress('Creating folder \''+folderName+'\'...', 70)
            folder = prj.rootFolder.dataFolders.add(folderName)
            print('... '+folderName)    
        elif ret==adsk.core.DialogResults.DialogNo:
            return localFileName
        elif ret==adsk.core.DialogResults.DialogCancel:
            dontAskAgain = True
            return None
    
    if not folder or not folder.isValid:
        print('Failed creating folder '+folderName)    
        ui.messageBox('Unable to create folder  \'' +folderName+ '\'  :(\n'
                        'Try again later or please create it manualy')
        return localFileNameOffline

    print('Found folder '+folderName)    

    print('Looking for file '+fileName)    
    doc = None
    for f in folder.dataFiles:
        f = adsk.core.DataFile.cast(f)
        if fileName in f.name:
            print('File found '+fileName)    
            return f

    print('File not found '+fileName)    
    print('Creating file... '+fileName)    
    progress('Creating file \''+fileName+'\'...', 90)
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    print('... '+fileName)
    if doc.saveAs(fileName, folder,' ',' '):
        pass
    else:
        ui.messageBox('Unable to save \''+fileName+'\' file')
    doc.close(False)
    print('... '+fileName)    

    print('Looking for file '+fileName)    
    for f in folder.dataFiles:
        f = adsk.core.DataFile.cast(f)
        if fileName in f.name:
            print('File found ' + f.name)    
            #ui.messageBox('VisualStyles preferences file created','Success')
            fo=folder
            global folder
            folder = fo
            return f

    print('File not found '+fileName+' Using offline file')    
    return localFileNameOffline


def getPreferencesFile(forceLocal=False):
    global configFile
    
    print('getPreferencesFile forceLocal='+str(forceLocal)+' configFile='+str(configFile))
    if configFile and isinstance(configFile,adsk.core.DataFile) and configFile.isValid and not forceLocal:
        print('getPreferencesFile return cached \'configFile\'')
        return configFile
    else:
        try:
            configFile = getPrefFile(forceLocal)
        except:
            print('Failed getPrefFile')
            configFile =localFileNameOffline
            
    return configFile


def getConfig():
    cfg = None

    file = getPreferencesFile()
    if isinstance(file, str):
        cfg = validateConfig(cfg, file==localFileName)
        if not os.path.exists(file):
            print('Creating local file '+file)
            saveLocal(cfg, file)
        else:
            cfg = readLocal(file)
    elif isinstance(file, adsk.core.DataFile):
        prefs = file.name.split('=')
        if len(prefs)==1:
            pass
            #ui.messageBox('first run')
        elif len(prefs)==2:
            cfg = prefs[1]
            offlineCfg = readLocal(localFileNameOffline)
            if offlineCfg and offlineCfg!=cfg:
                print('Cloud preferences outdated. Using offline local data')
                cfg = offlineCfg
        else:
            print('error getConfig()')
            #ui.messageBox('error getConfig()')
    else:
        pass
    
    progress(None)
 
    global config
    config = validateConfig(cfg)
    return config
    
    
def setConfig(cfg):
    app = adsk.core.Application.get()
    ui  = app.userInterface

    cfg_old = cfg    
    cfg = validateConfig(cfg)
    print('setConfig()' + str(cfg_old) + ' ' + cfg)
    
    if cfg[localPreferencesLocation]=='1': 
        global dontAskAgain
        dontAskAgain =False
        forceLocal = True
    else:
        try:
            if os.path.exists(localFileName):
                os.unlink(localFileName) #remove local preferences
        except:
            pass
        forceLocal = False
    
    file = getPreferencesFile(forceLocal)
    if isinstance(file, str):
        if cfg[localPreferencesLocation] != '1':
            cfg = validateConfig(cfg, file==localFileName)
        saveLocal(cfg, file)
    elif isinstance(file, adsk.core.DataFile):
        prefs = file.name.split('=')
        newFileName =''
        if len(prefs)==1 or len(prefs)==2:
            newFileName = prefs[0]+'='+cfg
            try:
                if file and file.isValid:
                    print('Setting cloud file name to: '+ newFileName)
                    file.name = newFileName
                    saveLocal(cfg, localFileNameOffline)
            except:
                print('Failed setting cloud file name to: '+ newFileName)
                print('Trying again...')
                try:
                    file = getPrefFile(forceLocal)
                    if file and isinstance(file,file, adsk.core.DataFile) and file.isValid:
                        print('Setting cloud file name to: '+ newFileName)
                        file.name = newFileName
                        saveLocal(cfg, localFileNameOffline)
                    elif isinstance(file,str):
                        cfg = validateConfig(cfg, file==localFileName)
                        saveLocal(cfg, file)
                except:
                    print('Failed getPrefFile or file.name = newFileName')
                    saveLocal(cfg, localFileNameOffline)
            finally:
                progress(None)

        else:
            ui.messageBox('error setConfig()') 
    else:
        global config
        config = cfg
    progress(None)
    
    
def validateConfig(cfg=None, forceLocal=False):
    init_config = '1'*visualStylesCmdCount + '0'
    if not cfg:
        return validateConfig(init_config, forceLocal)

    out=list(init_config)
    i =0
    for init in init_config:
        if i<len(cfg) and (cfg[i]=='1' or cfg[i]=='0'):
            out[i] = cfg[i]
        else:
            out[i] = init
        i +=1
    if forceLocal:
        out[localPreferencesLocation]='1'
        ConfigControl = commandControlByIdForNav(VSS_CmdId)
        if ConfigControl and ConfigControl.isValid:
            cmdDef = adsk.core.ListControlDefinition.cast(ConfigControl.commandDefinition.controlDefinition)
            if cmdDef and cmdDef.isValid:
                cmdDef.listItems.item(localPreferencesLocation).isSelected = True
    return ''.join(out)
    
    
def saveLocal(cfg, filename):
    print('Saving local file '+filename)
    try:
        with open(filename,'w') as f:
            f.write(cfg)
        if filename==localFileName and os.path.exists(localFileNameOffline):
            os.unlink(localFileNameOffline)
    except:
        print('Failed saving local file '+filename)


def readLocal(fileName):
    cfg =None
    try:
        print('Reading file '+fileName)
        with open(fileName,'r') as f:
            cfg = f.read()
    except:
        print('Failed reading local file')
    return cfg



def run(context):
    print('Init...') 
    ui = None
    
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        class CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self, cmd):
                super().__init__()
                self.cmd = cmd
            def notify(self, args):
                try:
                    arg_cmd = args.command
                    onExecute = ExecuteHandler(self.cmd)
                    arg_cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self, cmd):
                super().__init__()
                self.cmd = cmd
            def notify(self, args):
                try:  
                    # Set visual style of active viewport
                    app = adsk.core.Application.get()
                    app.activeViewport.visualStyle = self.cmd.vs
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                        
                       
        class Lst_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = Lst_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class Lst_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:  
                    ConfigControl = commandControlByIdForNav(VSS_CmdId)
                    cmdDef = adsk.core.ListControlDefinition.cast(ConfigControl.commandDefinition.controlDefinition)
                    cfg=''
                    for item in cmdDef.listItems:
                        cfg += '1' if item.isSelected else '0'
                       
                    pos =3
                    global config, clicksInARow, logToFile, _tmpPath
                    if config and len(config)>pos+1 and len(cfg)>pos+1:
                        if config[:pos]+config[pos+1:]==cfg[:pos]+cfg[pos+1:]:
                            clicksInARow +=1
                            if clicksInARow>=6 and not logToFile:
                                logToFile =True
                                print('Dumping to file')
                                ui.messageBox('Log dumped to: '+_tmpPath+'\nFurther loging to this file is on')
                        else:
                            clicksInARow =0
                                
                    setConfig(cfg)
                    updateVisibility(cfg)

                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                        

        config = getConfig() 
        
        # Get the UserInterface object and the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions

        navBar = ui.toolbars.itemById('NavToolbar')
        toolbarControlsNAV = navBar.controls    


        print('Creating Visual Styles Setup dropdown')
        viewDisplayCommand = toolbarControlsNAV.itemById('ViewDisplayCommand')
        id = VSS_CmdId           
        ConfigControl = viewDisplayCommand.controls.itemById(id)

        if not ConfigControl:
            lstCmd = cmdDefs.itemById(id)
            if not lstCmd:
                lstCmd = cmdDefs.addListDefinition(id, cmds[id].name,adsk.core.ListControlDisplayTypes.CheckBoxListType)
            
            onCommandCreated = Lst_CreatedHandler()
            lstCmd.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)
            viewDisplayControls = adsk.core.ToolbarControls.cast(viewDisplayCommand.controls)
            ConfigControl = viewDisplayControls.addCommand(lstCmd,'ViewVisualStyleCommand')
            ConfigControl.isVisible = True
            cmdDef = adsk.core.ListControlDefinition.cast(ConfigControl.commandDefinition.controlDefinition)
            cmdDef.isVisible = True
            i=0
            for id in cmdIds:
                if id!= VSS_CmdId: # and not(dontAskAgain and id==LP_CmdId):
                    cmdDef.listItems.add(cmds[id].name, True if config[i]!='0' else False)
                    i +=1

        print('Creating Visual Styles buttons')
        buttons = []            
        separator = None
        i =0            

        for id in cmdIds:
            cmd = cmds[id]
            if id!= VSS_CmdId:
                control = toolbarControlsNAV.itemById(id)

                if not control:
                    cmdDef = cmdDefs.itemById(id)
                    if not cmdDef:
                        tooltip = ''
                        if cmd == LP_CmdId:
                            tooltip = os.getcwd+localFileName
                        cmdDef = cmdDefs.addButtonDefinition(cmd.id, cmd.name, tooltip,(commandResources + cmd.res) if cmd.res else '')
        
                    if not separator:
                        # Add separator once      
                        separator = toolbarControlsNAV.addSeparator()
                        separator.isVisible = True
                    
                    onCommandCreated = CreatedHandler(cmd)
                    cmdDef.commandCreated.add(onCommandCreated)
                    # keep the handler referenced beyond this function
                    handlers.append(onCommandCreated)
                    control = toolbarControlsNAV.addCommand(cmdDef)
                    control.isVisible = True if config[i]=='1' else False
                    i +=1
                    buttons.append(control)            
            
        
        print('Creating workspace change event handler')
        class WorkspaceActivatedHandler(adsk.core.WorkspaceEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    work = adsk.core.Workspace.cast(args.workspace)
                    if work.isValid and ui:                        
                        global hideAll
                        hideAll = True if work.name.lower() =='compare' else False
                        print('Workspace changeto to '+ work.name.lower())
                        updateVisibility()                     
                        
                except:
                    if ui:
                        ui.messageBox('WorkspaceActivatedHandler failed: {}'.format(traceback.format_exc()))
                        
        def updateVisibility(_config=None):
            global hideAll, config
            print('updateVisibility config='+str(config) +' '+str(_config))
            if _config:
               config = _config

            if config:           
                i =0
                anyVisible = False
                for b in config:
                    if i<len(buttons) and buttons[i] and buttons[i].isValid:
                        buttons[i].isVisible = (True if b=='1' else False) and  not hideAll
                        anyVisible |= buttons[i].isVisible
                        i +=1
                    
                if separator and separator.isValid:
                    separator.isVisible = anyVisible
            
                                             
        workspaceActivated = WorkspaceActivatedHandler()
        ui.workspaceActivated.add(workspaceActivated)
        handlers.append(workspaceActivated)
        
        print('Init completed.') 


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    print('stopping...')
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        objArrayNav = []
        
        for cmdId in cmdIds:
            commandControlNav_ = commandControlByIdForNav(cmdId)
            if commandControlNav_:
                objArrayNav.append(commandControlNav_)
    
            commandDefinitionNav_ = commandDefinitionById(cmdId)
            if commandDefinitionNav_:
                objArrayNav.append(commandDefinitionNav_)
            
        for obj in objArrayNav:
            destroyObject(ui, obj)
        print('stopped.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    
            
def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox('tobeDeleteObj is not a valid object')


def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandDefinition id is not specified')
        return None
    commandDefinitions_ = ui.commandDefinitions
    commandDefinition_ = commandDefinitions_.itemById(id)
    return commandDefinition_

def commandControlByIdForNav(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    toolbars_ = ui.toolbars
    toolbarNav_ = toolbars_.itemById('NavToolbar')
    toolbarControls_ = toolbarNav_.controls
    toolbarControl_ = toolbarControls_.itemById(id) 

    if toolbarControl_ is not None:
        return toolbarControl_
    
    viewDisplayCommand = toolbarControls_.itemById('ViewDisplayCommand')
    viewVisualStyleConfigCommand = viewDisplayCommand.controls.itemById(VSS_CmdId)

    if viewVisualStyleConfigCommand is not None:
        return viewVisualStyleConfigCommand
    
    
    

# Logfile 
_tmpPath =None
_tmpBuff =[]

def print(_str, delete=False):
    global _tmpPath, _tmpBuff

    if delete:
        if _tmpPath and len(_tmpPath)>10 and os.path.exists(_tmpPath):
            os.unlink(_tmpPath)
            _tmpPath =None
        _tmpBuff =[]

    log =''
    if _str:
        t = datetime.datetime.now().strftime('%c.%f')[:-4]
        log = t+' '+ _str + '\n'
        
    if logToFile:
        if not _tmpPath:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='visualstyles_', suffix='.log') as t:
                if t and t.file and t.name:
                    _tmpPath = t.name
            
        if _tmpPath:
    #        with open('t:/visualstyles-out.log','a') as f:
            with open(_tmpPath,'a') as f:
                if len(_tmpBuff)>0:
                    f.writelines(_tmpBuff)
                    _tmpBuff =[]
                f.write(log)
    else:
        _tmpBuff.append(log)   