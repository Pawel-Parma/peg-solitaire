import pickle
import os
import threading as th
import time as t

from natsort import humansorted
import customtkinter as ctk
from PIL import Image
import pyautogui

from configuration import *
from src.board import *


# Implement Board Solution


class App:
    def __init__(self):
        # main root
        self.board = Board()
        self.picked_pieces = [[0] * self.board.size for _ in range(self.board.size)]
        self.board_frame_list = [[0] * self.board.size for _ in range(self.board.size)]
        self.board_label_list = [[0] * self.board.size for _ in range(self.board.size)]
        self.playing, self.history_current_place = 0, -1
        self.move, self.history = [], []
        self.board_solution = []

        self.root = ctk.CTk()
        self.root.title(TITLE)
        self.root.iconbitmap(LOGO_PATH)
        self.root.geometry(f"{WIDTH}x{HEIGHT}-{0}+{0}")
        self.root.minsize(WIDTH, HEIGHT)
        ctk.set_appearance_mode("dark")

        self.placed_image = ctk.CTkImage(dark_image=Image.open(PLACED_IMAGE_PATH), size=GAME_IMAGE_SIZE)
        self.blank_image = ctk.CTkImage(dark_image=Image.open(BLANK_IMAGE_PATH), size=GAME_IMAGE_SIZE)
        self.picked_image = ctk.CTkImage(dark_image=Image.open(PICKED_IMAGE_PATH), size=GAME_IMAGE_SIZE)

        self.main_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.main_frame.pack()
        self.name_label = ctk.CTkLabel(self.main_frame, text=TITLE, font=("Comic Sans", 60),
                                       text_color=COLOR_ORANGE)
        self.name_label.pack(pady=10)

        self.game_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.game_frame.pack(side="left")

        for j in range(self.board.size + 2):
            for k in range(self.board.size + 2):
                if 0 < j < 8:
                    board_place_part_frame = ctk.CTkFrame(self.game_frame, corner_radius=0,
                                                          fg_color=COLOR_CYAN, border_width=20,
                                                          border_color=COLOR_CYAN_DARK, width=100, height=40)
                    board_place_part_frame.grid(column=j + 1, row=k)

                    board_place_part_label = ctk.CTkLabel(board_place_part_frame, text=f"{chr(65 + j - 1)}",
                                                          font=("", 30), width=GAME_IMAGE_SIZE[0], height=40)
                    board_place_part_label.pack(pady=3, padx=3)

                else:
                    board_place_part_frame = ctk.CTkFrame(self.game_frame, corner_radius=0,
                                                          fg_color=COLOR_CYAN, border_width=20,
                                                          border_color=COLOR_CYAN_DARK, width=100, height=40)
                    board_place_part_frame.grid(column=j + 1, row=k)

                    board_place_part_label = ctk.CTkLabel(board_place_part_frame, text=f"{8 - k}"
                    if not (k in (0, 8)) else "", font=("", 30),
                                                          width=40 if j in (0, 8) else GAME_IMAGE_SIZE[0],
                                                          height=40 if k in (0, 8) else GAME_IMAGE_SIZE[1])
                    board_place_part_label.pack(pady=3, padx=3)

        for i in range(7):
            for j in range(7):
                board_frame_part = ctk.CTkFrame(self.game_frame, corner_radius=0, fg_color=COLOR_CYAN,
                                                border_width=10, border_color=COLOR_CYAN_DARK,
                                                width=100, height=100)
                board_frame_part.bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))
                self.board_frame_list[i][j] = board_frame_part
                board_frame_part.grid(column=j + 2, row=i + 1)

                board_label_part = ctk.CTkLabel(board_frame_part, text="", width=GAME_IMAGE_SIZE[0],
                                                height=GAME_IMAGE_SIZE[1])
                board_label_part.bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))
                self.board_label_list[i][j] = board_label_part
                board_label_part.pack(pady=3, padx=3)

        self.update_board()

        self.rules_button = ctk.CTkButton(self.main_frame, text='Rules', font=("", 40), fg_color=COLOR_CYAN,
                                          hover_color=COLOR_CYAN_DARK, command=self.rules)
        self.rules_button.place(y=20, x=0)
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.action_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.right_buttons_1_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_1_widgets_frame.pack()
        self.play_setpos_button = ctk.CTkButton(self.right_buttons_1_widgets_frame, text='Play', font=("", 40),
                                                fg_color=COLOR_CYAN,
                                                hover_color=COLOR_CYAN_DARK, command=self.play, width=240)
        self.play_setpos_button.pack(side="left", pady=5)
        self.reset_pos_button = ctk.CTkButton(self.right_buttons_1_widgets_frame, text='Reset', font=("", 40),
                                              fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                              command=lambda: self.confirm("reset"))
        self.reset_pos_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_2_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_2_widgets_frame.pack()
        self.save_button = ctk.CTkButton(self.right_buttons_2_widgets_frame, text='Save', font=("", 40),
                                         fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK, width=240,
                                         command=lambda: self.confirm("save"))
        self.save_button.pack(side="left", pady=5)
        self.load_button = ctk.CTkButton(self.right_buttons_2_widgets_frame, text='Load', font=("", 40),
                                         fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                         command=self.load)
        self.load_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_3_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_3_widgets_frame.pack()
        self.solution_button = ctk.CTkButton(self.right_buttons_3_widgets_frame, text='Solution', font=("", 40),
                                             fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK, width=240,
                                             command=lambda: self.confirm("solution"))
        self.solution_button.pack(side="left", pady=5)
        self.solve_button = ctk.CTkButton(self.right_buttons_3_widgets_frame, text='Solve', font=("", 40),
                                          fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                          command=lambda: self.confirm("solve"))
        self.solve_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_4_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_4_widgets_frame.pack()
        self.undo_button = ctk.CTkButton(self.right_buttons_4_widgets_frame, text='Undo', font=("", 40),
                                         fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                         command=self.undo, width=240)
        self.undo_button.pack(side="left", pady=5)
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.redo_button = ctk.CTkButton(self.right_buttons_4_widgets_frame, text='Redo', font=("", 40),
                                         fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                         command=self.redo)
        self.redo_button.pack(side="left", padx=10, pady=5)
        self.root.bind("<Control-y>", lambda e: self.redo())

        self.balls_counter_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.balls_counter_frame.pack()
        self.balls_counter_label = ctk.CTkLabel(self.balls_counter_frame, text="Current Balls: 0\n"
                                                                               "Initial Balls: 0",
                                                font=("", 35), text_color=COLOR_ORANGE)
        self.balls_counter_label.pack(pady=10)

        # rules root
        self.rules_root = ctk.CTkToplevel()
        self.rules_root.title(TITLE)
        self.rules_root.after(201, lambda: self.rules_root.iconbitmap(LOGO_PATH))
        self.rules_root.geometry(f"{750}x{380}-{0}+{0}")
        self.rules_root.resizable(False, False)
        self.rules_root.attributes('-topmost', True)
        self.rules_root.protocol("WM_DELETE_WINDOW", self.rules_exit)

        self.rules_main_frame = ctk.CTkFrame(self.rules_root, fg_color="transparent")
        self.rules_main_frame.pack()
        self.name_rules_label = ctk.CTkLabel(self.rules_main_frame, text="Rules", text_color=COLOR_ORANGE,
                                             font=("", 60))
        self.name_rules_label.pack()
        self.rules_label = ctk.CTkLabel(self.rules_main_frame, text_color=COLOR_ORANGE, font=("", 26),
                                        text="Place the balls in the holes.\nThe middle hole must remain empty.\n"
                                             "You can start playing from anywhere on the board.\n"
                                             "You move by \'jumping\' one ball over another ball,\n"
                                             "which is then removed from the board.\n"
                                             "You can only move horizontally or vertically, not diagonally.\n"
                                             "The game is over when no more \'jumps\' are possible.\n"
                                             "You win the game when there is just one ball left on the board,\n "
                                             "which must be in the middle hole.\n")
        self.rules_label.pack()

        # game end root
        self.game_end_text1_strvar = ctk.StringVar()
        self.game_end_text2_strvar = ctk.StringVar()

        self.game_end_root = ctk.CTkToplevel()
        self.game_end_root.title(TITLE)
        self.game_end_root.after(201, lambda: self.game_end_root.iconbitmap(LOGO_PATH))
        self.game_end_root.geometry(f"{550}x{180}-{0}+{0}")
        self.game_end_root.resizable(False, False)
        self.game_end_root.attributes('-topmost', True)
        self.game_end_root.protocol("WM_DELETE_WINDOW", self.game_end_exit)

        self.game_end_main_frame = ctk.CTkFrame(self.game_end_root, fg_color="transparent")
        self.game_end_main_frame.pack()
        self.game_end_congrats_label = ctk.CTkLabel(self.game_end_main_frame, textvariable=self.game_end_text1_strvar,
                                                    text_color=COLOR_ORANGE, font=("", 60))
        self.game_end_congrats_label.pack(pady=5)
        self.name_game_end_label = ctk.CTkLabel(self.game_end_main_frame, textvariable=self.game_end_text2_strvar,
                                                text_color=COLOR_CYAN, font=("", 60))
        self.name_game_end_label.pack(pady=5)

        # confirm root
        self.confirm_flavour_strvar = ctk.StringVar()

        self.confirm_root = ctk.CTkToplevel()
        self.confirm_root.title(TITLE)
        self.confirm_root.after(201, lambda: self.confirm_root.iconbitmap(LOGO_PATH))
        self.confirm_root.geometry("750x200")
        self.confirm_root.resizable(False, False)
        self.confirm_root.attributes("-topmost", True)
        self.confirm_root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        self.confirm_main_frame = ctk.CTkFrame(self.confirm_root, fg_color="transparent")
        self.confirm_main_frame.pack()
        self.confirm_root_label = ctk.CTkLabel(self.confirm_main_frame, text="Are you sure you want to proceed",
                                               font=("", 40), text_color=COLOR_ORANGE)
        self.confirm_root_label.pack(pady=20)
        self.confirm_root_yes_button = ctk.CTkButton(self.confirm_main_frame, text='Yes', font=("", 40),
                                                     fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                                     command=self.confirm_root_yes_button_pressed)

        self.confirm_root_yes_button.pack(side="left", padx=70, pady=25)
        self.confirm_root_no_button = ctk.CTkButton(self.confirm_main_frame, text='No', font=("", 40),
                                                    fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                                    command=self.confirm_exit)
        self.confirm_root_no_button.pack(side="right", padx=70, pady=25)

        # save root
        self.blocked = ["<", ">", ":", ";", "\"", "\'", "/", "\\", "|", "?", "*", ",", "."]
        self.load_folder_name = None
        self.save_text1 = "Type in a file name\n"
        self.save_text2 = "File with this name already exists\n" \
                          "Type in another file name"
        self.save_text3 = "The file name is incorrect\n" \
                          "Type in another file name"
        self.save_dir_name = ""

        try:
            os.mkdir("saves")

        except:
            pass

        self.dialog_root = ctk.CTkToplevel()
        self.dialog_root.title(TITLE)
        self.dialog_root.after(201, lambda: self.dialog_root.iconbitmap(LOGO_PATH))
        self.dialog_root.geometry("640x280")
        self.dialog_root.resizable(False, False)
        self.dialog_root.attributes("-topmost", True)
        self.dialog_root.protocol("WM_DELETE_WINDOW", self.save_exit)

        self.dialog_root_label = ctk.CTkLabel(self.dialog_root, text=self.save_text1, font=("", 40),
                                              text_color=COLOR_ORANGE)
        self.dialog_root_label.pack(pady=20)
        self.dialog_root_entry = ctk.CTkEntry(self.dialog_root, width=350, height=40)
        self.dialog_root_entry.pack()
        self.dialog_root_ok_button = ctk.CTkButton(self.dialog_root, text='Ok', font=("", 40),
                                                   fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                                   command=self.dialog_root_ok_button_pressed)
        self.dialog_root_ok_button.pack(side="left", padx=70, pady=25)
        self.dialog_root_cancel_button = ctk.CTkButton(self.dialog_root, text='Cancel', font=("", 40),
                                                       fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK,
                                                       command=self.save_exit)
        self.dialog_root_cancel_button.pack(side="right", padx=70, pady=25)

        # load root
        self.load_strvar = ctk.StringVar()
        self.list_of_saves = []

        self.load_root = ctk.CTkToplevel()
        self.load_root.title(TITLE)
        self.load_root.after(201, lambda: self.load_root.iconbitmap(LOGO_PATH))
        self.load_root.geometry(f"{800}x{550}-{0}+{0}")
        self.load_root.resizable(False, False)
        self.load_root.attributes('-topmost', True)
        self.load_root.protocol("WM_DELETE_WINDOW", self.load_exit)

        self.load_root_main_frame = ctk.CTkFrame(self.load_root, fg_color="transparent")
        self.load_root_main_frame.pack()
        self.load_root_label = ctk.CTkLabel(self.load_root_main_frame, text="Load saves", font=("", 60),
                                            text_color=COLOR_ORANGE)
        self.load_root_label.pack(pady=20)

        self.load_root_saves_frame_1 = ctk.CTkFrame(self.load_root_main_frame, fg_color="transparent")
        self.load_root_saves_frame_1.pack()
        self.show_load_saves_page()
        self.load_root_load_button = ctk.CTkButton(self.load_root_main_frame, text='Load', font=("", 40),
                                                   fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK, width=200,
                                                   command=lambda: self.confirm("load"))
        self.load_root_load_button.pack(side="left", padx=70, pady=30)
        self.load_root_delete_button = ctk.CTkButton(self.load_root_main_frame, text='Delete', font=("", 40),
                                                     fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_DARK, width=200,
                                                     command=lambda: self.confirm("delete"))
        self.load_root_delete_button.pack(side="right", padx=70, pady=30)

        # solution root
        self.solution_root = ctk.CTkToplevel()
        self.solution_root.title(TITLE)
        self.solution_root.after(201, lambda: self.solution_root.iconbitmap(LOGO_PATH))
        self.solution_root.geometry(f"{750}x{380}-{0}+{0}")
        self.solution_root.resizable(False, False)
        self.solution_root.attributes('-topmost', True)
        self.solution_root.protocol("WM_DELETE_WINDOW", self.solution_exit)

        self.solution_main_frame = ctk.CTkFrame(self.solution_root, fg_color="transparent")
        self.solution_main_frame.pack()
        self.name_solution_label = ctk.CTkLabel(self.solution_main_frame, text="Solution",
                                                text_color=COLOR_ORANGE, font=("", 60))
        self.name_solution_label.pack()
        self.solution_label = ctk.CTkLabel(self.solution_main_frame, text_color=COLOR_CYAN, font=("", 30),
                                           text="")
        self.solution_label.pack(pady=10)

    def square_pressed(self, y, x):
        if self.playing:
            self.move.append((y, x))
            if self.board[y, x] == 1:
                for i, j in self.move:
                    self.picked_pieces[i][j] = 0

                if len(self.move) > 1:
                    self.move = []

                else:
                    self.picked_pieces[y][x] = 1

            else:
                if len(self.move) == 2:
                    if self.board.is_move_legal(self.move) == 1:
                        self.picked_pieces = [[0] * self.board.size for _ in range(self.board.size)]
                        self.board.move(self.move)
                        self.history_tracker("move", self.move)

                    else:
                        for i, j in self.move:
                            self.picked_pieces[i][j] = 0

                self.move = []
                self.balls_counter_update(2)

        else:
            self.board.interact(y, x)
            self.balls_counter_update(1)
            self.history_tracker("interact", (y, x))

        self.update_board()
        if self.playing and self.board.is_end():
            self.game_end()

    def update_board(self):
        for i, v1 in enumerate(self.board):
            for j, v2 in enumerate(v1):
                if v2 == 1:
                    if self.picked_pieces[i][j] == 1:
                        self.board_label_list[i][j].configure(image=self.picked_image)

                    else:
                        self.board_label_list[i][j].configure(image=self.placed_image)

                elif v2 == 0:
                    self.board_label_list[i][j].configure(image=self.blank_image)

                else:
                    self.board_frame_list[i][j].unbind("<Button-1>")
                    self.board_label_list[i][j].unbind("<Button-1>")

        self.root.update_idletasks()

    def inactivate_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.board_frame_list[i][j].unbind("<Button-1>")
                self.board_label_list[i][j].unbind("<Button-1>")

    def activate_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.board_frame_list[i][j].bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))
                self.board_label_list[i][j].bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))

    def game_end(self):
        if self.board.is_won():
            self.game_end_text1_strvar.set("Congratulations!!!!!")
            self.game_end_text2_strvar.set("You Won!!!")

        else:
            self.game_end_text1_strvar.set("What a shame")
            self.game_end_text2_strvar.set("You Lost")

        self.play()
        self.game_end_root.state("normal")
        self.game_end_root.lift()

    def game_end_exit(self):
        self.game_end_root.state("withdrawn")

    def balls_counter_update(self, state):
        if state == 1:
            self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                    f"Initial Balls: {self.board.count(1)}")
            return

        elif state == 2:
            b = 1 if self.board.count(1) == 9 else 0

        elif state == 3:
            b = -1 if self.board.count(1) == 10 else 0

        else:
            b = 0

        self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n" +
                                                self.balls_counter_label.cget('text')
                                                [len(f"Current Balls: {self.board.count(1)}\n") + b:])

    def rules(self):
        if self.rules_root.winfo_viewable() == 0:
            self.rules_root.state("normal")
            self.rules_root.lift()

        else:
            self.rules_exit()

    def rules_exit(self):
        self.rules_root.state("withdrawn")

    def play(self):
        if self.playing:
            self.playing = 0
            self.play_setpos_button.configure(text="Play")

        else:
            if self.board.is_legal_to_start():
                self.playing = 1
                self.play_setpos_button.configure(text="Set Position")

    def reset(self):
        if self.playing:
            self.play()

        self.game_end_exit()
        self.board.reset_board()
        self.history, self.history_current_place = [], -1
        self.update_board()
        self.balls_counter_update(1)

    def save(self):
        self.dialog_root.state("normal")
        self.dialog_root.grab_set()
        self.dialog_root.lift()
        self.dialog_root.after(150, self.dialog_root_entry.focus)
        self.dialog_root_entry.select_present()
        self.dialog_root_entry.delete(0, "end")

    def save_exit(self):
        self.dialog_root.state("withdrawn")
        self.dialog_root.grab_release()

    def dialog_root_ok_button_pressed(self):
        self.save_dir_name = self.dialog_root_entry.get()

        if self.save_dir_name is not None:
            if self.is_text_legal(self.save_dir_name):
                if self.save_dir_name not in os.listdir("saves"):
                    self.all_exit()
                    self.root.after(170, lambda: self.save_data(self.save_dir_name))
                    self.history, self.history_current_place = [], -1
                    self.save_exit()

                else:
                    self.dialog_root_label.configure(text=self.save_text2)

            else:
                self.dialog_root_label.configure(text=self.save_text3)

        else:
            self.save_exit()

    def all_exit(self):
        exits = self.rules_exit, self.game_end_exit, self.confirm_exit, \
            self.save_exit, self.load_exit, self.solution_exit

        for fun in exits:
            fun()

    def is_text_legal(self, text):
        if len(text) > 0:
            if not text[0].isdigit():
                if "".join([y for y in text if y not in self.blocked]) == text:
                    return 1

        return 0

    def save_data(self, text):
        dir_name = f"saves\\{text}\\"
        os.mkdir(dir_name)

        with open(f"{dir_name}{text}.dat", 'wb') as f:
            x, y = self.game_frame.winfo_rootx(), self.game_frame.winfo_rooty()
            w, h = self.game_frame.winfo_width(), self.game_frame.winfo_height()
            img = pyautogui.screenshot(region=(x, y, w, h))
            img.save(f"{dir_name}{text}.jpg")
            pickle.dump(self.board.lightweight_serialize(), f)

    def load(self):
        if self.load_root.winfo_viewable() == 0:
            self.load_root.state("normal")
            self.load_root.lift()
            self.list_of_saves = humansorted(os.listdir("saves"))
            self.load_folder_name = ""
            self.show_load_saves_page()

        else:
            self.load_root.state("withdrawn")

    def save_mouse_wheel(self, event):
        if self.load_root_saves_frame_2._parent_canvas.xview() != (0.0, 1.0):
            self.load_root_saves_frame_2.parent_canvas.xview("scroll", -int(event.delta / 36), "units")

        return "break"

    def show_load_saves_page(self):
        try:
            self.load_root_saves_frame_2.pack_forget()

        except:
            pass

        self.load_root_saves_frame_2 = ctk.CTkScrollableFrame(self.load_root_saves_frame_1, fg_color="transparent",
                                                              orientation="horizontal", width=700, height=300)
        self.load_root_saves_frame_2._parent_canvas.configure(yscrollincrement=20, xscrollincrement=20)
        self.load_root_saves_frame_2.bind("<MouseWheel>", self.save_mouse_wheel)
        self.load_root_saves_frame_2.pack()

        self.load_strvar.set(None)
        self.save_radiobutton_list = []

        for i, save in enumerate(self.list_of_saves):
            save_frame = ctk.CTkFrame(self.load_root_saves_frame_2, fg_color="transparent")
            save_frame.bind("<Button-1>", lambda e, name=i: self.save_chosen_other(name))
            save_frame.bind("<MouseWheel>", self.save_mouse_wheel)
            save_frame.pack(side="left", padx=30 * (i % 2))
            save_image = ctk.CTkImage(dark_image=Image.open(f"saves\\{save}\\{save}.jpg"), size=(210, 210))
            save_image_label = ctk.CTkLabel(save_frame, text=None, image=save_image)
            save_image_label.bind("<Button-1>", lambda e, name=i: self.save_chosen_other(name))
            save_image_label.bind("<MouseWheel>", self.save_mouse_wheel)
            save_image_label.pack()
            save_radiobutton = ctk.CTkRadioButton(save_frame, text=save, variable=self.load_strvar, value=save,
                                                  command=self.save_chosen_radiobutton, font=("", 30),
                                                  text_color=COLOR_ORANGE, hover_color=COLOR_CYAN_DARK,
                                                  fg_color=COLOR_CYAN, radiobutton_width=25, radiobutton_height=25,
                                                  corner_radius=5)
            self.save_radiobutton_list.append(save_radiobutton)
            save_radiobutton.bind("<MouseWheel>", self.save_mouse_wheel)
            save_radiobutton.pack(side="left", padx=5, pady=5)

        self.load_folder_name = None

    def save_chosen_other(self, name):
        self.save_radiobutton_list[name].invoke()

    def save_chosen_radiobutton(self):
        self.load_folder_name = self.load_strvar.get()

    def load_board(self):
        self.reset()
        with open(f"saves\\{self.load_folder_name}\\{self.load_folder_name}.dat", "rb") as f:
            self.board = pickle.load(f)

        self.update_board()
        self.balls_counter_update(1)

    def delete_board(self):
        os.remove(f"saves\\{self.load_folder_name}\\{self.load_folder_name}.dat")
        os.remove(f"saves\\{self.load_folder_name}\\{self.load_folder_name}.jpg")
        os.rmdir(f"saves\\{self.load_folder_name}")
        self.list_of_saves = humansorted(os.listdir("saves"))
        self.load_folder_name = None
        self.show_load_saves_page()

    def load_exit(self):
        self.load_root.state("withdrawn")
        self.load_folder_name = None

    def confirm(self, flavour):
        if self.load_folder_name is not None or flavour not in ["load", "delete"]:
            self.confirm_flavour_strvar.set(flavour)
            self.confirm_root.state("normal")
            self.confirm_root.grab_set()
            self.confirm_root.lift()

    def confirm_exit(self):
        self.confirm_root.state("withdrawn")
        self.confirm_root.grab_release()

    def confirm_root_yes_button_pressed(self):
        self.confirm_exit()

        if self.confirm_flavour_strvar.get() == "solution":
            self.solution()

        elif self.confirm_flavour_strvar.get() == "solve":
            self.solve()

        elif self.confirm_flavour_strvar.get() == "reset":
            self.reset()

        elif self.confirm_flavour_strvar.get() == "save":
            self.save()

        elif self.confirm_flavour_strvar.get() == "load":
            self.load_board()

        elif self.confirm_flavour_strvar.get() == "delete":
            self.delete_board()

    def solution(self):
        s = t.perf_counter()
        moves = list(enumerate(translate_moves(self.board.solution())))
        print(t.perf_counter() - s)
        size = 50
        text = "None"

        if moves:
            size = 30
            text = [f"{i + 1}. {move}, " + "\n" * ((i % 5 + 1) // 5) for i, move in moves]
            text = "".join(text)

        self.solution_label.configure(text=text, font=("", size))
        self.solution_root.state("normal")
        self.solution_root.lift()

    def solution_exit(self):
        self.solution_root.state("withdrawn")

    def __solve_helper(self):
        for move in self.board_solution:
            t.sleep(1)
            self.board.move(move)
            self.history_tracker("move", move)
            self.update_board()
            self.balls_counter_update(2)

        self.buttons_on_off("enabled")
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.play()
        self.activate_board()
        self.game_end()

    def solve(self):
        self.inactivate_board()
        self.buttons_on_off("disabled")
        self.root.unbind("<Control-y>")
        self.root.unbind("<Control-z>")
        self.board_solution = self.board.solution()

        thread = th.Thread(name="Solve_Thread", target=self.__solve_helper)
        thread.start()

    def buttons_on_off(self, state):
        self.solve_button.configure(state=state)
        self.play_setpos_button.configure(state=state)
        self.reset_pos_button.configure(state=state)
        self.save_button.configure(state=state)
        self.load_button.configure(state=state)
        self.solution_button.configure(state=state)
        self.undo_button.configure(state=state)
        self.redo_button.configure(state=state)

    def history_tracker(self, state, action):
        if self.history_current_place == len(self.history) - 1:
            if state == "interact":
                self.history.append(("I", action))

            elif state == "move":
                self.history.append(("M", action))

            self.history_current_place += 1

        elif self.history_current_place < len(self.history) - 1:
            if self.history[self.history_current_place][1] != action:
                self.history = self.history[:self.history_current_place + 1 if
                                                self.history_current_place < len(self.history) - 1 else None]

                if state == "interact":
                    self.history.append(("I", action))

                elif state == "move":
                    self.history.append(("M", action))

            self.history_current_place += 1

    def __undo_helper(self):
        if self.history_current_place > -1:
            if self.history[self.history_current_place][0] == "I":
                if self.playing == 0:
                    y, x = self.history[self.history_current_place][1]
                    self.board.interact(y, x)
                    self.history_current_place -= 1
                    self.balls_counter_update(1)

            elif self.history[self.history_current_place][0] == "M":
                move = self.history[self.history_current_place][1]
                (_, _), (y2, x2), (_, _) = process_move(move)
                self.board.interact(y2, x2)
                self.board.move(move[::-1])
                self.board.interact(y2, x2)
                self.history_current_place -= 1
                if self.playing == 1:
                    self.balls_counter_update(3)

                else:
                    self.balls_counter_update(1)

            self.update_board()

        t.sleep(0.5)

    def undo(self):
        thread = th.Thread(name="Undo_Thread", target=self.__undo_helper)
        thread.start()

    def __redo_helper(self):
        if self.history_current_place < len(self.history) - 1:
            if self.history[self.history_current_place + 1][0] == "I":
                if self.playing == 0:
                    y, x = self.history[self.history_current_place + 1][1]
                    self.board.interact(y, x)
                    self.history_current_place += 1
                    self.balls_counter_update(1)

            elif self.history[self.history_current_place + 1][0] == "M":
                move = self.history[self.history_current_place + 1][1]
                self.board.move(move)
                self.history_current_place += 1
                if self.playing == 1:
                    self.balls_counter_update(2)

                else:
                    self.balls_counter_update(1)

            self.update_board()

        t.sleep(0.5)

    def redo(self):
        thread = th.Thread(name="Redo_Thread", target=self.__redo_helper)
        thread.start()

    def run(self):
        self.root.after(301, self.all_exit)
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard Interrupt, exiting...")
