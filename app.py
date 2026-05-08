from flask import Flask, render_template, request, jsonify, session
import random
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Game 1: Guess the Number
class GuessNumberGame:
    def __init__(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False
        
    def guess(self, number):
        self.attempts += 1
        if number == self.secret_number:
            self.game_over = True
            return {'result': 'win', 'message': f'Зөв! {self.attempts} удаа оролдлоо.'}
        elif number < self.secret_number:
            return {'result': 'higher', 'message': 'Илүү их тоо'}
        else:
            return {'result': 'lower', 'message': 'Илүү бага тоо'}
    
    def reset(self):
        self.__init__()

# Game 2: Rock, Paper, Scissors
class RockPaperScissorsGame:
    def __init__(self):
        self.choices = ['Чулуу', 'Даавуу', 'Хайч']
        self.scores = {'player': 0, 'computer': 0}
    
    def play(self, player_choice):
        computer_choice = random.choice(self.choices)
        
        if player_choice == computer_choice:
            result = 'тэнцсэн'
        elif (player_choice == 'Чулуу' and computer_choice == 'Хайч') or \
             (player_choice == 'Даавуу' and computer_choice == 'Чулуу') or \
             (player_choice == 'Хайч' and computer_choice == 'Даавуу'):
            result = 'ялалт'
            self.scores['player'] += 1
        else:
            result = 'ялагдал'
            self.scores['computer'] += 1
        
        return {
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result,
            'scores': self.scores
        }

# Game 3: Image Guess
class ImageGuessGame:
    def __init__(self):
        self.images = {
            '🐶': 'нохой',
            '🐱': 'муур',
            '🦁': 'арслан',
            '🐯': 'бар',
            '🐸': 'нь хонь',
            '🦋': 'эрвүүлэнцэг',
            '🐢': 'яст мэлхий',
            '🐧': 'пингвин'
        }
        self.current_emoji = None
        self.attempts = 0
        self.correct = False
        self.new_round()
    
    def new_round(self):
        self.current_emoji = random.choice(list(self.images.keys()))
        self.attempts = 0
        self.correct = False
    
    def guess(self, answer):
        self.attempts += 1
        correct_answer = self.images[self.current_emoji]
        
        if answer.lower() == correct_answer.lower():
            self.correct = True
            return {'result': 'win', 'message': f'Зөв! Энэ бол "{correct_answer}"'}
        else:
            if self.attempts >= 3:
                return {'result': 'lose', 'message': f'Гарчээ. Хариулт нь "{correct_answer}"'}
            return {'result': 'wrong', 'message': f'Буруу. Дахин оролдоё. ({self.attempts}/3)'}

# Game 4: Fibonacci Riddle
class FibonacciGame:
    def __init__(self):
        self.scores = 0
        self.question_count = 0
        self.generate_question()
    
    def generate_question(self):
        self.question_count += 1
        n = random.randint(5, 12)
        self.fib_sequence = self.get_fibonacci(n)
        self.missing_index = random.randint(1, len(self.fib_sequence) - 2)
        self.correct_answer = self.fib_sequence[self.missing_index]
    
    def get_fibonacci(self, n):
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib
    
    def get_question(self):
        sequence = self.fib_sequence.copy()
        sequence[self.missing_index] = '?'
        return sequence
    
    def answer(self, user_answer):
        try:
            answer = int(user_answer)
            if answer == self.correct_answer:
                self.scores += 1
                self.generate_question()
                return {'result': 'correct', 'score': self.scores}
            else:
                return {'result': 'wrong', 'correct': self.correct_answer}
        except:
            return {'result': 'invalid', 'message': 'Буруу оролдоо'}

# Game 5: Maze
class MazeGame:
    def __init__(self):
        self.maze = [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', 'S', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'E', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]
        self.player_pos = [1, 1]
        self.moves = 0
    
    def move(self, direction):
        new_pos = self.player_pos.copy()
        
        if direction == 'up':
            new_pos[0] -= 1
        elif direction == 'down':
            new_pos[0] += 1
        elif direction == 'left':
            new_pos[1] -= 1
        elif direction == 'right':
            new_pos[1] += 1
        
        if self.maze[new_pos[0]][new_pos[1]] != '#':
            self.player_pos = new_pos
            self.moves += 1
            
            if self.player_pos == [7, 8]:
                return {'status': 'win', 'moves': self.moves}
            return {'status': 'moving', 'pos': self.player_pos, 'moves': self.moves}
        
        return {'status': 'blocked', 'message': 'Дам гаж чадахгүй'}
    
    def get_maze_state(self):
        maze_copy = [row.copy() for row in self.maze]
        maze_copy[self.player_pos[0]][self.player_pos[1]] = 'P'
        return maze_copy

# Game instances
games = {
    'guess_number': GuessNumberGame(),
    'rock_paper_scissors': RockPaperScissorsGame(),
    'image_guess': ImageGuessGame(),
    'fibonacci': FibonacciGame(),
    'maze': MazeGame()
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<game_name>')
def game(game_name):
    if game_name not in games:
        return "Game not found", 404
    return render_template(f'{game_name}.html')

# Game endpoints
@app.route('/api/guess_number/guess', methods=['POST'])
def guess_number_guess():
    data = request.json
    number = int(data.get('number', 0))
    result = games['guess_number'].guess(number)
    return jsonify(result)

@app.route('/api/guess_number/reset', methods=['POST'])
def guess_number_reset():
    games['guess_number'].reset()
    return jsonify({'status': 'reset'})

@app.route('/api/rock_paper_scissors/play', methods=['POST'])
def rock_paper_scissors_play():
    data = request.json
    choice = data.get('choice')
    result = games['rock_paper_scissors'].play(choice)
    return jsonify(result)

@app.route('/api/image_guess/guess', methods=['POST'])
def image_guess_guess():
    data = request.json
    answer = data.get('answer')
    result = games['image_guess'].guess(answer)
    return jsonify(result)

@app.route('/api/image_guess/get_emoji', methods=['GET'])
def image_guess_get_emoji():
    return jsonify({'emoji': games['image_guess'].current_emoji})

@app.route('/api/image_guess/new_round', methods=['POST'])
def image_guess_new_round():
    games['image_guess'].new_round()
    return jsonify({'emoji': games['image_guess'].current_emoji})

@app.route('/api/fibonacci/get_question', methods=['GET'])
def fibonacci_get_question():
    question = games['fibonacci'].get_question()
    return jsonify({'question': question, 'score': games['fibonacci'].scores})

@app.route('/api/fibonacci/answer', methods=['POST'])
def fibonacci_answer():
    data = request.json
    answer = data.get('answer')
    result = games['fibonacci'].answer(answer)
    return jsonify(result)

@app.route('/api/maze/get_state', methods=['GET'])
def maze_get_state():
    maze_state = games['maze'].get_maze_state()
    return jsonify({'maze': maze_state, 'moves': games['maze'].moves})

@app.route('/api/maze/move', methods=['POST'])
def maze_move():
    data = request.json
    direction = data.get('direction')
    result = games['maze'].move(direction)
    return jsonify(result)

@app.route('/api/maze/reset', methods=['POST'])
def maze_reset():
    games['maze'] = MazeGame()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
