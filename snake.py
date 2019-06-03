import numpy as np

class Snake():
	def __init__(self, board_size):
		self.board_size = board_size
		self.length = 1
		self.body = [(0, 0)] # replace with something random
		self.direction = 0
		self.right = 0
		self.left  = 1
		self.up    = 2
		self.down  = 3

	def addNode(self, prev_tail):
		self.length += 1
		self.body.append(prev_tail)

	def updateHead(self):
		if self.direction == self.right:
			self.body[0] = (self.body[0][0], self.body[0][1] + 1)
		elif self.direction == self.left:
			self.body[0] = (self.body[0][0], self.body[0][1] - 1)
		elif self.direction == self.down:
			self.body[0] = (self.body[0][0] + 1, self.body[0][1])
		elif self.direction == self.up:
			self.body[0] = (self.body[0][0] - 1, self.body[0][1])

	def withinBounds(self):
		if self.body[0][0] == self.board_size:
			return False
		elif self.body[0][0] < 0:
			return False
		elif self.body[0][1] == self.board_size:
			return False
		elif self.body[0][1] < 0:
			return False
		return True

	def isDead(self):
		if not self.withinBounds():
			return True
		for i in range(1, len(self.body)):
			if self.body[0] == self.body[i]:
				return True
		return False

	def updateSnake(self):
		for i in reversed(range(1, len(self.body))):
			self.body[i] = self.body[i - 1]
		self.updateHead()


class Board():
	def __init__(self, board_size):
		self.board_size = board_size
		self.snake = Snake(board_size)
		self.board = np.zeros((board_size, board_size))
		self.reward_pos = tuple(np.random.randint(
				self.board_size, size=2))
		self.rewards = 0
		self.board[self.reward_pos] = 2
		self.board[self.snake.body[0]] = 1

	def step(self, action):
		reward = 0
		self.snake.direction = action
		self.board[self.snake.body[-1]] = 0
		prev_tail = self.snake.body[-1]
		self.snake.updateSnake()
		if self.snake.body[0] == self.reward_pos:
			reward = 1
			self.reward_pos = tuple(np.random.randint(
				self.board_size, size=2))
			while self.reward_pos in self.snake.body:
				self.reward_pos = tuple(np.random.randint(
					self.board_size, size=2))
			self.rewards += 1
			self.snake.addNode(prev_tail)
			self.board[prev_tail] = 1
		if self.snake.isDead():
			return self.board, reward, True
		self.board[self.snake.body[0]] = 1
		return self.board, reward, False

	def reset(self):
		self.board_size = self.board_size
		self.snake = Snake(self.board_size)
		self.board = np.zeros((self.board_size, self.board_size))
		self.reward_pos = tuple(np.random.randint(
				self.board_size, size=2))
		self.rewards = 0
		self.board[self.reward_pos] = 2
		self.board[self.snake.body[0]] = 1
		return self.board


if __name__ == '__main__':
	env = Board(4)
	i = 0
	action = 0
	rewards = 0
	while True:
		i += 1
		obs, reward, done = env.step(action)
		rewards += reward
		if done:
			print("Episode terminated after {0} steps with {1} reward".format(i, rewards))
			break