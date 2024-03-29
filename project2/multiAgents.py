# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    score = successorGameState.getScore()
    #numAgent = successorGameState.getNumAgents()
    distanceToFood = [manhattanDistance(newPos,food) for food in newFood.asList()]
    distanceToGhost = manhattanDistance(newPos,newGhostStates[0].getPosition())
    score_Food = 5.0
    score_Ghost = -5.0
    if distanceToGhost > 0:
        score += score_Ghost / distanceToGhost
    if len(distanceToFood) != 0:
        score += score_Food / min(distanceToFood)
    return score

    #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def findMax(gameState, depth, numGhosts):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(0)
        value = float("-inf")
        for move in movement:
            value = max(value, findMin(gameState.generateSuccessor(0, move),depth -1, 1,numGhosts))
        return value

    def findMin(gameState, depth, nowAgent, numGhost):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(nowAgent)
        value = float("inf")
        if nowAgent == numGhost:
            for move in movement:
                value = min(value, findMax(gameState.generateSuccessor(nowAgent,move), depth - 1, numGhost))
        else:
            for move in movement:
                value = min(value, findMin(gameState.generateSuccessor(nowAgent, move), depth, nowAgent + 1, numGhost))
        return value

    movement = gameState.getLegalActions()
    numGhost = gameState.getNumAgents() - 1
    action = Directions.STOP
    score = float("-inf")
    for move in movement:
        nextState = gameState.generateSuccessor(0, move)
        tempScore = score
        score = max(score, findMin(nextState, self.depth, 1, numGhost))
        if score > tempScore:
            action = move
    return action

    #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def findMax(gameState, depth, numGhosts, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(0)
        value = float("-inf")
        for move in movement:
            value = max(value, findMin(gameState.generateSuccessor(0, move),depth -1, 1,numGhosts, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def findMin(gameState, depth, nowAgent, numGhost, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(nowAgent)
        value = float("inf")
        if nowAgent == numGhost:
            for move in movement:
                value = min(value, findMax(gameState.generateSuccessor(nowAgent,move), depth - 1, numGhost, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        else:
            for move in movement:
                value = min(value, findMin(gameState.generateSuccessor(nowAgent, move), depth, nowAgent + 1, numGhost, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value

    movement = gameState.getLegalActions()
    numGhost = gameState.getNumAgents() - 1
    action = Directions.STOP
    score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    for move in movement:
        nextState = gameState.generateSuccessor(0, move)
        tempScore = score
        score = max(score, findMin(nextState, self.depth, 1, numGhost, alpha, beta))
        if score > tempScore:
            action = move
    return action
    #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    def findMax(gameState, depth, numGhosts):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(0)
        value = float("-inf")
        for move in movement:
            value = max(value, findExp(gameState.generateSuccessor(0, move),depth - 1, 1, numGhosts))
        return value

    def findExp(gameState, depth, nowAgent, numGhost):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        movement = gameState.getLegalActions(nowAgent)
        prob = len(movement)
        value = 0
        if nowAgent == numGhost:
            for move in movement:
                p = prob
                value += p * findMax(gameState.generateSuccessor(nowAgent,move), depth - 1, numGhost)
        else:
            for move in movement:
                p = prob
                value += p * findExp(gameState.generateSuccessor(nowAgent, move), depth, nowAgent + 1, numGhost)
        return value

    movement = gameState.getLegalActions()
    numGhost = gameState.getNumAgents() - 1
    action = Directions.STOP
    score = float("-inf")
    for move in movement:
        nextState = gameState.generateSuccessor(0, move)
        tempScore = score
        score = max(score, findExp(nextState, self.depth, 1, numGhost))
        if score > tempScore:
            action = move
    return action
    #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    I added a scaredTimer in the function to record the remaining scared time,
    and changed the ghost score into a more valuable positive. This would drive
    pacman to chase the ghost. After the scared time, I set the value of new capsule
    more valuable than the normal food, so the pacman would go for capsule in advance
    and longer the scared time of the ghosts
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition ()
  newFood = currentGameState.getFood ()
  newGhostStates = currentGameState.getGhostStates ()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  newCapsules = currentGameState.getCapsules ()

  score = currentGameState.getScore ()
  numAgent = currentGameState.getNumAgents ()
  distanceToFood = [manhattanDistance (newPos, food) for food in newFood.asList ()]
  distanceToCapsules = [manhattanDistance (newPos, capsule) for capsule in newCapsules]
  distanceToGhost = manhattanDistance (newPos, newGhostStates[0].getPosition ())
  if newScaredTimes[0] == 0:
      score_Capsule = 7.0
      score_Food = 3.0
      score_Ghost = -10.0
      if distanceToGhost > 0:
          score += score_Ghost / distanceToGhost
      if len (distanceToFood):
          score += score_Food / min (distanceToFood)
      if len (distanceToCapsules):
          score += score_Capsule / min (distanceToCapsules)
  elif newScaredTimes[0] <= 5:
      score_Capsule = 5.0
      score_Food = 5.0
      score_Ghost = -10.0
      if distanceToGhost > 0:
          score += score_Ghost / distanceToGhost
      if len (distanceToFood):
          score += score_Food / min (distanceToFood)
      if len (distanceToCapsules):
          score += score_Capsule / min (distanceToCapsules)
  else:
      score_Capsule = 1.0
      score_Food = 1.0
      score_Ghost = 100.0
      if distanceToGhost > 0:
          score += score_Ghost / distanceToGhost
      if len (distanceToFood):
          score += score_Food / min (distanceToFood)
      if len (distanceToCapsules):
          score += score_Capsule / min (distanceToCapsules)
  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

