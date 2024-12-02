from invokepy import dispatcher

@dispatcher.register("cmd1")
def cmd1(arg1: str):
    print("cmd1", arg1)

@dispatcher.register("cmd2")
def cmd2():
    print("cmd2")


dispatcher.execute("cmd1")