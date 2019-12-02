from importlib import reload, import_module  # Python 3.4+ only.

if __name__ == '__main__':
    day = input('enter number of day: ').strip().rjust(2, '0')

    module = import_module(f'day{day}_solve')

    # https://stackoverflow.com/questions/5597836/embed-create-an-interactive-python-shell-inside-a-python-program
    import code
    variables = globals().copy()
    variables.update(locals())
    console = code.InteractiveConsole({
        'm': module,
    })
    
    def_r = compile('''
from importlib import reload

def r():
    global m
    m = reload(m)''', '<string>', 'exec')
    console.runcode(def_r)

    console.write(
        f'Starting debug session for `day{day}_solve`. Use "r()" to reload module.\n')
    console.interact()
