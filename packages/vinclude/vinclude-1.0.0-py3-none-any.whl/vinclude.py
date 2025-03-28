#!/usr/bin/python3

import subprocess
    
source_extensions = [".c", ".cc", ".cp", ".cpp", ".cxx", ".c++"] # From https://www.ibm.com/docs/en/xl-c-and-cpp-aix/16.1?topic=cc-xl-input-output-files
header_extensions = [".h", ".hh", ".hp", ".hpp", ".hxx", ".h++"]
extensions = source_extensions + header_extensions

def main():
    print("Loading include graph...")

    # List occurrences of "#include"
    # ===

    includelist = subprocess.check_output(['grep', '-r', '--exclude-dir=".*"', '#include'], text=True)
    #includelist = subprocess.check_output(['git', 'grep', '#include'], text=True)


    # Build associations
    # ===

    # List of which files include which other files
    associations = {}

    # Track included files to print warning if header files are never included
    includes = []

    for entry in includelist.split("\n"):
        if ":#include" not in entry:
            continue
        
        if "<" in entry:
            continue

        try:
            _from, _to = entry.split(':#include "')
            _to = _to[:-1]
            if "/" in _to:
                _to = _to.split("/")[-1]
            
            if _to not in includes:
                includes.append(_to)
            
            if _from not in associations:
                associations[_from] = []
                
            associations[_from].append(_to)
        except ValueError:
            pass
    
    
    # Get all relevant files
    # ===

    cmd = ['find', '-not', '-path', '*/.*', '-type', 'f', '-printf', r"%P\n"]
    #cmd = ['git', 'ls-files']
    pathlist = \
        subprocess.check_output(cmd, text=True) \
            .split("\n")
    pathlist.sort()

    # Exclude non-C/non-C++ files
    pathlist = [path for path in pathlist if any([path.lower().endswith(ext) for ext in extensions])]


    # Build map of where each file is
    # ===

    # All top-level paths
    paths = {}
    # Filenames that occur at least twice (these can't be matched with this simple static analysis)
    doubles = []
    for path in pathlist:
        try:
            split_path = path.split("/")
            if len(split_path) <= 1:
                continue
            
            name = split_path[-1]
            
            # Print information if header files are not used
            if (not any([name.lower().endswith(ext) for ext in header_extensions])) and name not in includes:
                print("Seemingly unused:", path)
            
            if name in paths:
                doubles.append(name)
                print("Occurs twice: ", name)
                del paths[name]
            elif name not in doubles:
                paths[name] = path

        except ValueError:
            pass


    # Create list of toplevel folders
    # ===
    
    toplevels = {}

    for _from in pathlist:
        split_path = _from.split("/")
        
        if len(split_path) > 1:
            base = split_path[0]
            if base not in toplevels:
                toplevels[base] = []
            toplevels[base].append(_from)


    # Show UI
    # ===
    # Based on this great example by claymcleod: https://gist.github.com/claymcleod/b670285f334acd56ad1c
    import curses

    def draw_menu(stdscr):
        k = ""
        _filter = ""
        
        selected_index = 0
        selected_entry = 0
        detail_view = False
        fullscreen = False
        
        detail_x = 0
        detail_y = 0
        
        last_from = None
        last_to = None

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        
        pad = curses.newpad(100,100)
        pad2 = curses.newpad(100,100)

        while (k != 'q'):
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            
            pad.resize(height, width)
            pad2.resize(height, width)
            
            cursoryx = (0,0)
            
            # Interpret keyboard inputs
            # ===
            if k == "\t":
                detail_view = not detail_view
            elif k == "\n":
                fullscreen = not fullscreen
            elif detail_view:
                if k == '\x7f':
                    _filter = _filter[:max(len(_filter)-1,0)]
                elif len(k) == 1 and k != "\n":
                    _filter += k
                elif k == "KEY_BACKSPACE":
                    if len(_filter) > 0:
                        _filter = _filter[:-1] 
                elif k == "KEY_DOWN":
                    detail_y += 10
                elif k == "KEY_UP":
                    detail_y = max(detail_y - 10, 0)
                elif k == "KEY_RIGHT":
                    detail_x += 10
                elif k == "KEY_LEFT":
                    detail_x = max(detail_x - 10, 0)
            else:
                if k == "KEY_DOWN":
                    selected_index += 1
                    detail_x = 0
                    detail_y = 0
                elif k == "KEY_UP":
                    selected_index -= 1
                    detail_x = 0
                    detail_y = 0
                elif k == "KEY_RIGHT":
                    selected_entry += 1
                    detail_x = 0
                    detail_y = 0
                elif k == "KEY_LEFT":
                    selected_entry -= 1
                    detail_x = 0
                    detail_y = 0
            
            # Paint GUI
            # ===
            
            selected_index %= len(toplevels)
            
            try:
                last_from = ""
                last_to = ""
                pad.move(0,0)
                for i, base in enumerate(toplevels):
                    dependencies = []
                    
                    for _from in associations:
                        if not _from.startswith(base + "/"):
                            continue
                        
                        for _to in associations[_from]:
                            if _to in doubles and '???' not in dependencies:
                                dependencies = ['???'] + dependencies
                            
                            if _to not in paths:
                                continue
                            
                            split_path = paths[_to].split("/")
                            if len(split_path) <= 1:
                                continue
                            
                            _base = split_path[0]
                            
                            if _base not in dependencies:
                                dependencies.append(_base)
                                dependencies.sort()
                    
                    if selected_index == i:
                        pad.attron(curses.color_pair(1))
                        last_from = base
                        selected_entry %= max(1, len(dependencies))
                    
                    pad.addstr(base)
                    pad.attroff(curses.color_pair(1))
                    
                    pad.addstr(" -> ")
                    for j, dependency in enumerate(dependencies):
                        if selected_index == i and selected_entry == j:
                            pad.attron(curses.color_pair(3))
                            last_to = dependency
                        pad.addstr(dependency)
                        pad.attroff(curses.color_pair(3))
                        pad.addstr(" ")
                    pad.addstr("\n")

                pad2.clear()
                
                pad2.move(0,0)
                
                for _from in associations:
                    if not _from.startswith(last_from + "/"):
                        continue
                    
                    for _to in associations[_from]:
                        if _to in doubles:
                            _str = _from + " -> " + _to+" (filename occurs at least twice)\n"
                        elif _to not in paths:
                            continue
                        elif not paths[_to].startswith(last_to + "/"):
                            continue
                        else:
                            _str = _from + " -> " + paths[_to]+"\n"
                        
                        if len(_filter) > 0 and _filter not in _str:
                            continue
                        
                        y, x = pad2.getmaxyx()
                        pad2.resize(y + 1, max(x, len(_str)))
                        pad2.addstr(_str)
            except curses.error:
                pass
            
            if not fullscreen:
                if not detail_view:
                    stdscr.move(0, 0)
                    stdscr.vline("|", height//2-1)
                    curses.curs_set(0)
                else:
                    stdscr.move(height//2+2, 0)
                    stdscr.vline("|", height//2-3)
                    curses.curs_set(1)
            
            # Render status bar
            stdscr.attron(curses.color_pair(3))
            try:
                stdscr.addstr(height-1, 0, " " * (width-1))
                line = "vinclude.py | q: exit | tab: toggle detail view | enter: toggle fullscreen"
                if False: # debug output
                    line += " | Last input: " + str(repr(k))
                stdscr.addstr(height-1, 2, line)
            except curses.error:
                pass
            
            stdscr.attroff(curses.color_pair(3))
            
            if not fullscreen or detail_view:
                line_pos = 1 if fullscreen else height//2
                    
                stdscr.move(line_pos,0)
                stdscr.hline("=", width)
                stdscr.move(line_pos,3)
                stdscr.addstr(
                    " " \
                    + last_from + " -> " + last_to \
                    + " === Filter: '{}' ".format(_filter)
                )
                cursory, cursorx = stdscr.getyx()
                cursoryx = cursory, cursorx-2

            try:
                stdscr.refresh()
                if not fullscreen:
                    pad.refresh( 0,0, 1,3, height//2-2,width-3)
                    pad2.refresh( detail_y,detail_x, height//2+2,2, height-4,width-2)
                elif detail_view:
                    pad2.refresh( detail_y,detail_x, 3,2, height-2,width-2)
                else:
                    pad.refresh( 0,0, 2,3, height-3,width-3)
            
                if detail_view:
                    stdscr.move(*cursoryx)
            except curses.error:
                pass
            
            k = stdscr.getkey()

    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
