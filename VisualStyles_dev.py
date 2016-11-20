#Author - pawelzwronek(aka blowman3)
#Description - Quick change visuals style of active viewport
#Modified source of Show Hidden by Patrick Rainsberry

#Changelog
#v1.0 - Initial version
#v1.0.1 - Hiding buttons in 'COMPARE' workspace


import adsk.core, adsk.fusion, traceback

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

cmdIds = [S_CmdId, SHE_CmdId, SVEO_CmdId, W_CmdId, WHE_CmdId, WVEO_CmdId]

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
    
    

def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox('tobeDeleteObj is not a valid object')
            
def setVisualStyle(visualStyle):

    app = adsk.core.Application.get()
    app.activeViewport.visualStyle = visualStyle

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        vs = adsk.core.VisualStyles

        class S_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = S_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class S_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:  
                    setVisualStyle(vs.ShadedVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                        
        class SHE_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = SHE_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class SHE_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    setVisualStyle(vs.ShadedWithHiddenEdgesVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                        
        class SVEO_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = SVEO_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class SVEO_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    setVisualStyle(vs.ShadedWithVisibleEdgesOnlyVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                        
        class W_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = W_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class W_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    setVisualStyle(vs.WireframeVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                          
        class WHE_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = WHE_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class WHE_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    setVisualStyle(vs.WireframeWithHiddenEdgesVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                          
        class WVEO_CreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = WVEO_ExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)               
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))     

        class WVEO_ExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    setVisualStyle(vs.WireframeWithVisibleEdgesOnlyVisualStyle)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))   
                          
        
        # Get the UserInterface object and the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions

        navBar = ui.toolbars.itemById('NavToolbar')
        toolbarControlsNAV = navBar.controls
        
        S_Control = toolbarControlsNAV.itemById(S_CmdId)
        if not S_Control:
            S_cmdDef = cmdDefs.itemById(S_CmdId)
            if not S_cmdDef:
                S_cmdDef = cmdDefs.addButtonDefinition(S_CmdId, 'Shaded', '',commandResources + '/S')

            # Add separator once      
            Split_Control = toolbarControlsNAV.addSeparator()
            Split_Control.isVisible = True
            
            onCommandCreated = S_CreatedHandler()
            S_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            S_Control = toolbarControlsNAV.addCommand(S_cmdDef)
            S_Control.isVisible = True
        
        SHE_Control = toolbarControlsNAV.itemById(SHE_CmdId)
        if not SHE_Control:
            SHE_cmdDef = cmdDefs.itemById(SHE_CmdId)
            if not SHE_cmdDef:
                SHE_cmdDef = cmdDefs.addButtonDefinition(SHE_CmdId, 'Shaded with Hidden Edges', '',commandResources + '/SHE')
            onCommandCreated = SHE_CreatedHandler()
            SHE_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            SHE_Control = toolbarControlsNAV.addCommand(SHE_cmdDef)
            SHE_Control.isVisible = True
            
        SVEO_Control = toolbarControlsNAV.itemById(SVEO_CmdId)
        if not SVEO_Control:
            SVEO_cmdDef = cmdDefs.itemById(SVEO_CmdId)
            if not SVEO_cmdDef:
                SVEO_cmdDef = cmdDefs.addButtonDefinition(SVEO_CmdId, 'Shaded with Visible Edges Only', '',commandResources + '/SVEO')
            onCommandCreated = SVEO_CreatedHandler()
            SVEO_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            SVEO_Control = toolbarControlsNAV.addCommand(SVEO_cmdDef)
            SVEO_Control.isVisible = True
            
        W_Control = toolbarControlsNAV.itemById(W_CmdId)
        if not W_Control:
            W_cmdDef = cmdDefs.itemById(W_CmdId)
            if not W_cmdDef:
                W_cmdDef = cmdDefs.addButtonDefinition(W_CmdId, 'Wireframe', '',commandResources + '/W')
            onCommandCreated = W_CreatedHandler()
            W_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            W_Control = toolbarControlsNAV.addCommand(W_cmdDef)
            W_Control.isVisible = True
            
        WHE_Control = toolbarControlsNAV.itemById(WHE_CmdId)
        if not WHE_Control:
            WHE_cmdDef = cmdDefs.itemById(WHE_CmdId)
            if not WHE_cmdDef:
                WHE_cmdDef = cmdDefs.addButtonDefinition(WHE_CmdId, 'Wireframe with Hidden Edges', '',commandResources + '/WHE')
            onCommandCreated = WHE_CreatedHandler()
            WHE_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            WHE_Control = toolbarControlsNAV.addCommand(WHE_cmdDef)
            WHE_Control.isVisible = True
            
        WVEO_Control = toolbarControlsNAV.itemById(WVEO_CmdId)
        if not WVEO_Control:
            WVEO_cmdDef = cmdDefs.itemById(WVEO_CmdId)
            if not WVEO_cmdDef:
                WVEO_cmdDef = cmdDefs.addButtonDefinition(WVEO_CmdId, 'Wireframe with Visible Edges Only', '',commandResources + '/WVEO')
            onCommandCreated = WVEO_CreatedHandler()
            WVEO_cmdDef.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            WVEO_Control = toolbarControlsNAV.addCommand(WVEO_cmdDef)
            WVEO_Control.isVisible = True
            
            
        class WorkspaceActivatedHandler(adsk.core.WorkspaceEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    work = adsk.core.Workspace.cast(args.workspace)
                    if work.isValid and ui:                        
                        show = True
                        if work.name.lower() =='compare':
                            show = False
                            
                        if S_Control:
                            S_Control.isVisible = show
                        if SHE_Control:
                            SHE_Control.isVisible = show
                        if SVEO_Control:
                            SVEO_Control.isVisible = show
                        if W_Control:
                            W_Control.isVisible = show
                        if WHE_Control:
                            WHE_Control.isVisible = show
                        if WVEO_Control:
                            WVEO_Control.isVisible = show
                        if Split_Control:
                            Split_Control.isVisible = show
                        
                except:
                    if ui:
                        ui.messageBox('WorkspaceActivatedHandler failed: {}'.format(traceback.format_exc()))
                        
               
            
        workspaceActivated = WorkspaceActivatedHandler()
        ui.workspaceActivated.add(workspaceActivated)
        handlers.append(workspaceActivated)           
        


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
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

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
