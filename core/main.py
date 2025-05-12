from core import YangTraceCore


if __name__ == "__main__":
    target = input('Input your target location: ')
    if len(target) <= 3:
        print("Error：the target is too short")
        exit(1)
    try:
        YangTraceCore.traceroute(target)
    except YangTraceCore.socket.gaierror:
        print(f"Could not get the target:  {target}")