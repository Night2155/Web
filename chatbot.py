# -*- coding: utf-8 -*-
import aiml
import sys
import os
def get_module_dir(name):
    path = getattr(sys.modules[name], '__file__', None)
    if not path:
        raise AttributeError('module %s has not attribute __file__' % name)
    return os.path.dirname(os.path.abspath(path))
#alice_path = get_module_dir('aiml') + '\\botdata\\alice'
mybot_path = './chat_robot/'
#切换到语料库所在工作目录
# os.chdir(mybot_path)
# alice = aiml.Kernel()
# alice.learn("std-startup.xml")
# alice.respond('LOAD ALICE')
mybot = aiml.Kernel()
mybot.learn("./chat_robot/*.aiml")
mybot.respond('load aiml b')
while True:
    message = input("Enter your message >> ")
    if message == "quit":
        print("Bye Bye")
        exit()
    else:
        print(mybot.respond(message))