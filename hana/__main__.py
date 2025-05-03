# default entry point

def launch_api():
    try:
        from os import execlp
        execlp('python', 'python', '-i', '-c', 'import hana; from sys import version; print(f"python {version.split()[0]}, hana {hana.__version__}"); print("do hana.help or help(hana)")')
    except Exception as e:
        print(e)
        print("could not open default python interactive interpreter")
        print("falling back to python's code.interact()...")
    
    try:
        from sys import version
        from code import interact
        import hana
    
        banner = f"""(using fallback console. autocomplete may not be available)
python {version.split()[0]}, hana {hana.__version__}
do hana.help or help(hana)"""

        interact(banner=banner, local={'hana': hana})
	
    except Exception as e:
        print(e)
        print("could not open python interactive interpreter")
        print("exiting...")

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(prog='hana', description='toolkit/interactive python application for approximating the function of a graph')

	# mutually exclusive interface modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--api', action='store_true', help='launch API/CLI (default)')
    mode_group.add_argument('--gui', action='store_true', help='launch GUI (coming soon!)')
    mode_group.add_argument('--web', action='store_true', help='launch web interface (coming soon!)')

    parser.add_argument('-v', '--version', action='store_true', help='show version and exit')

    args = parser.parse_args()

    if args.version:
        from graphapproximator import __version__
        print(__version__)
        return

    if args.gui:
        print('GUI mode is not implemented yet')
        return

    elif args.web:
        print('Web mode is not implemented yet')
        return

    else:
        launch_api()

if __name__ == '__main__':
    main()
