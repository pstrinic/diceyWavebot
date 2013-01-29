from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner
import logging
import re
import random

def rollDie(dieSides):
  return random.randint(1, int(dieSides))

def parse(text):

  ret = "" 

  logging.debug(text);
  
  regex = "([\+\-])?\s*(?:(\d+)\s*\**\s*)d(\d+)(?:\s*([\+\-]\s*\d+))?"
  findRolls = re.compile(regex)
  rolls = findRolls.findall(text)
  allRolls = []

  for roll in rolls:
    diceRolls = []
    rollModifier = roll[0]
    rollCount = roll[1]
    dieSides = roll[2]
    try:
      modifier = int(roll[3])
    except IndexError:
      modifier = 0
    except ValueError:
      modifier = 0

    i = 0
    while i < int(rollCount):
      rollValue = rollDie(dieSides)
      diceRolls.append(rollValue)
      i += 1

    total = sum(diceRolls) + modifier

    if rollModifier == '-':
      allRolls.append(-total)
    else:
      allRolls.append(total)

    if modifier > 0:
      modifier = "+%s" % modifier
    elif modifier == 0:
      modifier = ''

    rollSummary = "%s%sd%s%s" % (rollModifier, rollCount, dieSides, modifier)

    ret += ("roll: %s (%s = %s%s) = %s" % (rollSummary, diceRolls, sum(diceRolls), modifier, total))
    ret += "\n"

  if len(rolls) > 1:
    ret += ("total: (%s) = %s" % (allRolls, sum(allRolls)))

  return ret

def OnRobotAdded(event, wavelet):
  wavelet.reply("Morning. Type 3d6+1, to roll 3x 6 sided dice and add 1 to the total. Typing 3d6+1-2d3+2, will also roll 2x 3 sided dice, add 2 and subtract the total from the first roll's total, etc.")

def OnBlipSubmitted(event, wavelet):
  blip = event.blip
  contents = blip.text

  reply = parse(contents)
  if len(reply):
    wavelet.reply(reply)

if __name__ == '__main__':
  myRobot = robot.Robot('Dicey Wave Bot',
      image_url='http://diceywavebot.appspot.com/assets/icon.png',
      profile_url='http://petarstrinic.com/dicey-wave-bot/')
  myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
  myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)

  appengine_robot_runner.run(myRobot, debug=True)
