import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import sys
from datetime import datetime

class UIWindowMod(pygame_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()


pygame.init()

pygame.display.set_caption('Quick Start - pygame_gui')
window_surface = pygame.display.set_mode((800, 480))

background = pygame.Surface((800, 480))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600), 'theme.json')

startStop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 125), (100, 50)),
                                            text='Start',
                                            manager=manager)                                          

time_list = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((275, 25), (500, 425)),
                                                item_list=[],
                                                manager=manager,
                                                allow_multi_select = False)
delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((65, 225), (120,50)),
                                             text='Delete log',
                                             manager=manager)

counter_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 300), (150, 100)),
                                            text="Times checked: " + str(len(time_list.item_list)),
                                            manager=manager)

confirm_window = UIWindowMod(rect=pygame.Rect((200, 125), (400, 200)),
                                              manager=manager,
                                              visible=False, draggable=False,
                                              window_display_title="Delete dialog")
confirm_window_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-20, -50), (400,200)),
                                                    manager=manager,
                                                    container=confirm_window,
                                                   parent_element=confirm_window,
                                                    text="Are you sure you want to delete the log?")

confirm_window_yes = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((85, 75), (200, 50)),
                                                  manager=manager,
                                                  container=confirm_window,
                                                  parent_element=confirm_window,
                                                  text="Yes, delete the log")
time_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((25, 50), (200, 100)),
                                         text="",
                                         manager=manager,
                                         object_id=ObjectID(object_id="#time_label"))

clock = pygame.time.Clock()
startTime = None
timeMode = 0

while True:
    time_delta = clock.tick(60)/1000.0
    time_label.set_text(datetime.now().strftime("%I:%M:%S %p"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if not confirm_window.visible:
                if event.ui_element == startStop_button:
                    if timeMode == 0:
                        timeMode = 1
                        startTime = datetime.now().strftime("%a, %m/%d/%Y %I:%M:%S %p")
                        startStop_button.set_text("Stop")
                    elif timeMode == 1:
                        timeMode = 0
                        startStop_button.set_text("Start")
                        new_item = startTime + " - " + datetime.now().strftime("%a, %m/%d/%Y %I:%M:%S %p")
                        time_list.add_items([new_item])
                        time_list.rebuild()
                        counter_label.set_text("Times checked: " + str(len(time_list.item_list)))
                elif event.ui_element == delete_button:
                    confirm_window.rebuild()
                    confirm_window.visible = True
                    confirm_window.show()
            else:
                if event.ui_element == confirm_window_yes:
                    if timeMode == 1:
                        timeMode = 0
                        startStop_button.set_text("Start")
                    time_list.set_item_list([])
                    time_list.rebuild()
                    counter_label.set_text("Times checked: " + str(len(time_list.item_list)))
                    confirm_window.visible = False
                    confirm_window.hide()
                    

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
