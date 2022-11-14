#0-9 0-9 : 10 +/- : 11 + : 12 - : 13 * : 14 / : 15 . : 16 = : 17 AC
import shutil
import random
buttonlist = {0 : '0', 1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5', 6 : '6', 7 : '7', 8 : '8', 9 : '9', 10 : 'R', 11 : '+' , 12 : '-', 13 : '*', 14 : '/', 15 : '.'}
testcase = [ [1,11,1], [1,2,3,11,4,5,6], [1,12,1], [1,2,3,12,4,5,6], [2,13,3], [1,2,3,13,4,5,6], [4,14,2], [1,14,3], [1,15,0,1,11,0,15,9,9], [1,15,9,9,12,0,15,9,9], [1,15,2,13,2,15,3], [1,15,2,14,3,15,4], [2,11,13,3], [4,12,14,2], [1,15,11,2], [1,15,2,15,1,12,0,15,1,15,2], [1,10,0,12,1,0], [1,10,0,10,14,1,0], [1,2,3,4,15,5,6,7,8,14,8,7,6,5,15,4,3,2,1], [1,2,3,4,15,5,6,7,8,13,8,7,6,5,15,4,3,2,1], [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,13,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9], [1,14,0] ]
def doTest(buttons, result, fixedexpression):
    terminalwidth = shutil.get_terminal_size().columns
    tries = 1000
    randomStr = []
    randomInt = []
    basicStr = []
    basicInt = []
    print('TEST STARTED'.center(terminalwidth, '+'))

    print('BASIC TEST STARTED'.center(terminalwidth, '-'))
    for i in range(len(testcase)):
        for j in range(len(testcase[i])):
            basicInt.append(testcase[i][j])
            basicStr.append(buttonlist[basicInt[-1]])
        print('INPUTTED:  ' + ' '.join(basicStr))
        for k in range(len(basicInt)):
            buttons[basicInt[k]].invoke()
        buttons[16].invoke()
        inputbuttons = fixedexpression.get()
        outputresult = result.get()
        buttons[17].invoke()
        basicStr = []
        basicInt = []
        print('EXPRESSION:  ' + inputbuttons, end = '   ')
        print('RESULT:  ' + outputresult, end = '\n\n')
    print('BASIC TEST ENDED'.center(terminalwidth, '-'), end = "\n\n\n")
    print('RANDOM TEST STARTED'.center(terminalwidth, '-'))
    for i in range(tries):
        length = random.randint(1, 20)
        for j in range(length):
            randomInt.append(random.randint(0, 15))
            randomStr.append(buttonlist[randomInt[-1]])
        print('INPUTTED:  ' + ' '.join(randomStr))
        for k in range(len(randomInt)):
            buttons[randomInt[k]].invoke()
        buttons[16].invoke()
        inputbuttons = fixedexpression.get()
        outputresult = result.get()
        buttons[17].invoke()
        randomStr = []
        randomInt = []
        print('EXPRESSION:  ' + inputbuttons, end = '   ')
        print('RESULT:  ' + outputresult, end = '\n\n')
    print('RANDOM TEST ENDED'.center(terminalwidth, '-'), end = "\n\n\n")
    print('ALL TEST ENDED'.center(terminalwidth, '+'))