import os
import inspect
from importlib import import_module


DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
moduleDIR = DIR + '\MODULES'

def findModule(data, dexActive):
    '''
    Check each module in the list
    Check each module till the validate function returns true
    return the moduleID of the valid module
    '''

    modules = listModules()

    for module in modules:
        if module == None:
            break

        mod = import_module(module)
        getID = getattr(mod, 'getID')
        validate = getattr(mod, 'validate')

        if validate(data, dexActive) == True:
            return getID()


    return False


def listModules():
    '''
    list all the modules from the MODULES directory
    Return the list
    '''

    rawmodules = []
    arrmodules = [None] * 100
    modules = []

    for file in os.listdir(moduleDIR):
        if os.path.splitext(file)[1] == '.py':
            module = os.path.splitext(file)[0]
            module = 'MODULES.'+module

            rawmodules.append(module)


    for mod in rawmodules:
        module = import_module(mod)
        getID = getattr(module, 'getID')

        arrmodules[int(getID())] = mod


    for mod in arrmodules:
        if mod != None:
            modules.append(mod)

    return modules
