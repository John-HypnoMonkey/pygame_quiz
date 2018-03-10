import pygame
import sys
from text_block import TextBlock
from answer_button import AnswerButton
from question_object import Question_Object


class GameState:
    menu, game, game_over = range(3)

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.question_height = 100
        self.answer_height = 50
        self.surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.mouse_handlers = []
        self.objects = []
        self.answer_objects = []
        self.current_question = None
        self.current_question_i = -1
        self.score = 0
        self.state = GameState.game
        self.questions = [Question_Object('World War I began in which year?', ('1923', '1938', '1917', '1914'), 3),
                          Question_Object('The Hundred Years War was fought between what two countries?',
                                          ('Italy and Carthage', 'England and Germany', 'France and England', 'Spain and France'), 2),
                          Question_Object('Who fought in the war of 1812?', ('Andrew Jackson', 'Arthur Wellsley', 'Otto von Bismarck', 'Napoleon'), 0)
                          ]
        self.score_text_block = TextBlock(500, 10, 250, 50, "Score: {0}/{1}".format(str(self.score), str(len(self.questions))))
        self.objects.append(self.score_text_block)
        self.nextQuestion()
        self.game_over_text_block = TextBlock(250, 250, 300, 50, "Game over")

    def update(self):
            for item in self.objects:
                item.update()

            for item in self.answer_objects:
                item.update()

    def draw(self):
        for item in self.objects:
            item.draw(self.surface)

        for item in self.answer_objects:
            item.draw(self.surface)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def addTextBlock(self, x, y, w, h, text):
        self.objects.append(TextBlock(x, y, w, h, text))

    def addAnswerButton(self, x, y, w, h, text, onclick_func, is_it_correct):
        button1 = AnswerButton(x, y, w, h, text, onclick_func, is_it_correct)
        self.answer_objects.append(button1)
        self.mouse_handlers.append(button1.handleMouseEvent)

    def checkAnswer(self, obj):
        if obj.is_it_correct_answer is True:
            self.score += 1
        self.score_text_block.text = "Score: {0}/{1}".format(str(self.score), str(len(self.questions)))
        self.nextQuestion()

    def gameOver(self):
        self.state = GameState.game_over
        self.cleanScreen()
        self.game_over_text_block.text = "Game over. Your score is {0}".format(str(self.score))
        self.objects.append(self.game_over_text_block)

    def cleanScreen(self):
        del self.answer_objects[:]
        del self.objects[:]
        del self.mouse_handlers[:]

    def nextQuestion(self):
        del self.answer_objects[:]
        del self.mouse_handlers[:]
        self.current_question_i += 1
        if self.current_question_i >= len(self.questions):
            self.gameOver()
        else:
            self.current_question = self.questions[self.current_question_i]
            self.addTextBlock(50, 70, 700, self.question_height,
                              self.current_question.question_text)

            answers = self.current_question.answers

            i = 0

            for item in answers:
                if self.current_question.correct_answer == i:
                    is_it_correct = True
                else:
                    is_it_correct = False

                self.addAnswerButton(50, self.question_height+80+i*(self.answer_height+10),
                                     700, self.answer_height, item, self.checkAnswer, is_it_correct)
                i += 1

    def run(self):
        while True:
            self.surface.fill((192, 192, 192))
            self.handleEvents()
            self.draw()
            self.update()
            pygame.display.update()
            self.clock.tick(60)


Game1 = Game()


Game1.run()
