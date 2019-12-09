from subprocess import Popen, PIPE
import time

control_f4_sequence = '''keydown Control_L
key F4
keyup Control_L
'''

shift_a_sequence = '''keydown Shift_L
key A
keyup Shift_L
'''
# single key
up_Key = '''key W
'''
down_Key = '''key S
'''
left_Key = '''key A
'''
right_Key = '''key D
'''
j_Key = '''key J
'''
k_Key = '''key K
'''
l_Key = '''key L
'''
# key down
up_KeyDown = '''keydown W
'''
down_KeyDown = '''keydown S
'''
left_KeyDown = '''keydown A
'''
right_KeyDown = '''keydown D
'''
j_KeyDown = '''keydown J
'''
k_KeyDown = '''keydown K
'''
l_KeyDown = '''keydown L
'''
# key up
up_KeyUp = '''keyup W
'''
down_KeyUp = '''keyup S
'''
left_KeyUp = '''keyup A
'''
right_KeyUp = '''keyup D
'''
j_KeyUp = '''keyup J
'''
k_KeyUp = '''keyup K
'''
l_KeyUp = '''keyup L
'''



def keypress(sequence):
    if isinstance(sequence, str):
        sequence = sequence.encode('ascii')
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

#keypress(shift_a_sequence)
#keypress(control_f4_sequence)
while (1):
    
    # Ballken
    keypress(down_KeyDown)
    time.sleep(0.05)
    keypress(right_KeyDown)
    time.sleep(0.05)
    keypress(down_KeyUp)
    time.sleep(0.05)
    keypress(k_KeyDown)
    time.sleep(0.1)
    keypress(right_KeyUp)
    keypress(k_KeyUp)

    time.sleep(5)

    # Holuken
    keypress(right_KeyDown)
    time.sleep(0.05)
    keypress(down_KeyDown)
    time.sleep(0.05)
    keypress(right_KeyUp)
    time.sleep(0.05)
    keypress(right_KeyDown)
    time.sleep(0.05)
    keypress(down_KeyUp)
    time.sleep(0.05)
    keypress(k_KeyDown)
    time.sleep(0.1)
    keypress(right_KeyUp)
    keypress(k_KeyUp)
    
    time.sleep(5)



