# Dependencies: natsort, customtkinter, pillow, pyautogui

from natsort import humansorted
from configuration import *
import customtkinter as ctk
import threading as th
from PIL import Image
from board import *
import pyautogui
import time as t
import pickle
import os


# Optimize everything and widget creaction more in __init__ with
# self.rules_root.state("withdrawn")
# normal, iconic, withdrawn, or zoomed
# root.winfo_viewable()
# root.state()

# Make save entry reset itself
# make repeating parts into methods
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

        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.root.title(title)
        self.root.iconbitmap(logo_path)
        self.root.geometry(f"{width}x{height}-{0}+{0}")
        self.root.minsize(width, height)

        self.placed_image = ctk.CTkImage(dark_image=Image.open(placed_image_path), size=game_image_size)
        self.blank_image = ctk.CTkImage(dark_image=Image.open(blank_image_path), size=game_image_size)
        self.picked_image = ctk.CTkImage(dark_image=Image.open(picked_image_path), size=game_image_size)

        self.main_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.main_frame.pack()
        self.name_label = ctk.CTkLabel(self.main_frame, text=title, font=("Comic Sans", 60),
                                       text_color=color_orange)
        self.name_label.pack(pady=10)

        self.game_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.game_frame.pack(side="left")

        for j in range(self.board.size + 2):
            for k in range(self.board.size + 2):
                if 0 < j < 8:
                    board_place_part_frame = ctk.CTkFrame(self.game_frame, corner_radius=0,
                                                          fg_color=color_cyan, border_width=20,
                                                          border_color=color_cyan_dark, width=100, height=40)
                    board_place_part_frame.grid(column=j + 1, row=k)

                    board_place_part_label = ctk.CTkLabel(board_place_part_frame, text=f"{chr(65 + j - 1)}",
                                                          font=("", 30), width=game_image_size[0], height=40)
                    board_place_part_label.pack(pady=3, padx=3)

                else:
                    board_place_part_frame = ctk.CTkFrame(self.game_frame, corner_radius=0,
                                                          fg_color=color_cyan, border_width=20,
                                                          border_color=color_cyan_dark, width=100, height=40)
                    board_place_part_frame.grid(column=j + 1, row=k)

                    board_place_part_label = ctk.CTkLabel(board_place_part_frame, text=f"{8 - k}"
                    if not (k == 0 or k == 8) else "", font=("", 30),
                                                          width=40 if j == 0 or j == 8 else game_image_size[0],
                                                          height=40 if k == 0 or k == 8 else game_image_size[1])
                    board_place_part_label.pack(pady=3, padx=3)

        for i, v1 in enumerate(self.board):
            for j, v2 in enumerate(v1):
                board_frame_part = ctk.CTkFrame(self.game_frame, corner_radius=0, fg_color=color_cyan,
                                                border_width=10, border_color=color_cyan_dark,
                                                width=100, height=100)
                board_frame_part.bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))
                self.board_frame_list[i][j] = board_frame_part
                board_frame_part.grid(column=j + 2, row=i + 1)

                board_label_part = ctk.CTkLabel(board_frame_part, text="", width=game_image_size[0],
                                                height=game_image_size[1])
                board_label_part.bind("<Button-1>", lambda e, y=i, x=j: self.square_pressed(y, x))
                self.board_label_list[i][j] = board_label_part
                board_label_part.pack(pady=3, padx=3)

        self.update_board()

        self.rules_button = ctk.CTkButton(self.main_frame, text='Rules', font=("", 40), fg_color=color_cyan,
                                          hover_color=color_cyan_dark, command=self.rules)
        self.rules_button.place(y=20, x=0)
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.action_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.right_buttons_1_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_1_widgets_frame.pack()
        self.play_setpos_button = ctk.CTkButton(self.right_buttons_1_widgets_frame, text='Play', font=("", 40),
                                                fg_color=color_cyan,
                                                hover_color=color_cyan_dark, command=self.play, width=240)
        self.play_setpos_button.pack(side="left", pady=5)
        self.reset_pos_button = ctk.CTkButton(self.right_buttons_1_widgets_frame, text='Reset', font=("", 40),
                                              fg_color=color_cyan, hover_color=color_cyan_dark,
                                              command=lambda: self.confirm_flavour_strvar.set("reset") or
                                              self.confirm("reset"))
        self.reset_pos_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_2_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_2_widgets_frame.pack()
        self.save_button = ctk.CTkButton(self.right_buttons_2_widgets_frame, text='Save', font=("", 40),
                                         fg_color=color_cyan, hover_color=color_cyan_dark, width=240,
                                         command=lambda: self.confirm_flavour_strvar.set("save") or
                                         self.confirm("save"))
        self.save_button.pack(side="left", pady=5)
        self.load_button = ctk.CTkButton(self.right_buttons_2_widgets_frame, text='Load', font=("", 40),
                                         fg_color=color_cyan, hover_color=color_cyan_dark,
                                         command=self.load)
        self.load_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_3_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_3_widgets_frame.pack()
        self.solution_button = ctk.CTkButton(self.right_buttons_3_widgets_frame, text='Sollution', font=("", 40),
                                             fg_color=color_cyan, hover_color=color_cyan_dark, width=240,
                                             command=lambda: self.confirm_flavour_strvar.set("solution") or
                                             self.confirm("solution"))
        self.solution_button.pack(side="left", pady=5)
        self.solve_button = ctk.CTkButton(self.right_buttons_3_widgets_frame, text='Solve', font=("", 40),
                                          fg_color=color_cyan, hover_color=color_cyan_dark,
                                          command=lambda: self.confirm_flavour_strvar.set("solve") or
                                          self.confirm("solve"))
        self.solve_button.pack(side="left", padx=10, pady=5)

        self.right_buttons_4_widgets_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.right_buttons_4_widgets_frame.pack()
        self.undo_button = ctk.CTkButton(self.right_buttons_4_widgets_frame, text='Undo', font=("", 40),
                                         fg_color=color_cyan, hover_color=color_cyan_dark,
                                         command=self.undo, width=240)
        self.undo_button.pack(side="left", pady=5)
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.redo_button = ctk.CTkButton(self.right_buttons_4_widgets_frame, text='Redo', font=("", 40),
                                         fg_color=color_cyan, hover_color=color_cyan_dark,
                                         command=self.redo)
        self.redo_button.pack(side="left", padx=10, pady=5)
        self.root.bind("<Control-y>", lambda e: self.redo())

        self.balls_counter_frame = ctk.CTkFrame(self.action_frame, fg_color='transparent')
        self.balls_counter_frame.pack()
        self.balls_counter_label = ctk.CTkLabel(self.balls_counter_frame, text="Current Balls: 0\n"
                                                                               "Initial Balls: 0",
                                                font=("", 35), text_color=color_orange)
        self.balls_counter_label.pack(pady=10)

        # rules root
        self.rules_root = ctk.CTkToplevel()
        self.rules_root.title(title)
        self.rules_root.after(201, lambda: self.rules_root.iconbitmap(logo_path))
        self.rules_root.geometry(f"{750}x{380}-{0}+{0}")
        self.rules_root.resizable(False, False)
        self.rules_root.attributes('-topmost', True)
        self.rules_root.protocol("WM_DELETE_WINDOW", lambda: self.rules_root.state("withdrawn"))

        self.rules_main_frame = ctk.CTkFrame(self.rules_root, fg_color="transparent")
        self.rules_main_frame.pack()
        self.name_rules_label = ctk.CTkLabel(self.rules_main_frame, text="Rules", text_color=color_orange,
                                             font=("", 60))
        self.name_rules_label.pack()
        self.rules_label = ctk.CTkLabel(self.rules_main_frame, text_color=color_orange, font=("", 26),
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
        self.game_end_root.title(title)
        self.game_end_root.after(201, lambda: self.game_end_root.iconbitmap(logo_path))
        self.game_end_root.geometry(f"{550}x{180}-{0}+{0}")
        self.game_end_root.resizable(False, False)
        self.game_end_root.attributes('-topmost', True)
        self.game_end_root.protocol("WM_DELETE_WINDOW", lambda: self.game_end_root.state("withdrawn"))

        self.game_end_main_frame = ctk.CTkFrame(self.game_end_root, fg_color="transparent")
        self.game_end_main_frame.pack()
        self.game_end_congrats_label = ctk.CTkLabel(self.game_end_main_frame, textvariable=self.game_end_text1_strvar,
                                                    text_color=color_orange, font=("", 60))
        self.game_end_congrats_label.pack(pady=5)
        self.name_game_end_label = ctk.CTkLabel(self.game_end_main_frame, textvariable=self.game_end_text2_strvar,
                                                text_color=color_cyan, font=("", 60))
        self.name_game_end_label.pack(pady=5)

        # confirm root
        self.confirm_flavour_strvar = ctk.StringVar()

        self.confirm_root = ctk.CTkToplevel()
        self.confirm_root.title(title)
        self.confirm_root.after(201, lambda: self.confirm_root.iconbitmap(logo_path))
        self.confirm_root.geometry("750x200")
        self.confirm_root.resizable(False, False)
        self.confirm_root.attributes("-topmost", True)
        self.confirm_root.protocol("WM_DELETE_WINDOW", lambda: self.confirm_root.state("withdrawn") or
                                   self.confirm_root.grab_release())

        self.confirm_main_frame = ctk.CTkFrame(self.confirm_root, fg_color="transparent")
        self.confirm_main_frame.pack()
        self.confirm_root_label = ctk.CTkLabel(self.confirm_main_frame, text="Are you sure you want to proceed",
                                               font=("", 40), text_color=color_orange)
        self.confirm_root_label.pack(pady=20)
        self.confirm_root_yes_button = ctk.CTkButton(self.confirm_main_frame, text='Yes', font=("", 40),
                                                     fg_color=color_cyan, hover_color=color_cyan_dark,
                                                     command=self.confirm_root_yes_button_pressed)

        self.confirm_root_yes_button.pack(side="left", padx=70, pady=25)
        self.confirm_root_no_button = ctk.CTkButton(self.confirm_main_frame, text='No', font=("", 40),
                                                    fg_color=color_cyan, hover_color=color_cyan_dark,
                                                    command=lambda: self.confirm_root.state("withdrawn") or
                                                    self.confirm_root.grab_release())
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

        self.dialog_root = ctk.CTkToplevel()
        self.dialog_root.title(title)
        self.dialog_root.after(201, lambda: self.dialog_root.iconbitmap(logo_path))
        self.dialog_root.geometry("640x280")
        self.dialog_root.resizable(False, False)
        self.dialog_root.attributes("-topmost", True)
        self.dialog_root.protocol("WM_DELETE_WINDOW", lambda: self.dialog_root.state("withdrawn") or
                                  self.dialog_root.grab_release())

        self.dialog_root_label = ctk.CTkLabel(self.dialog_root, text=self.save_text1, font=("", 40),
                                              text_color=color_orange)
        self.dialog_root_label.pack(pady=20)
        self.dialog_root_entry = ctk.CTkEntry(self.dialog_root, width=350, height=40)
        self.dialog_root_entry.pack()
        self.dialog_root.after(150, lambda: self.dialog_root_entry.focus())
        self.dialog_root_entry.select_present()

        self.dialog_root_ok_button = ctk.CTkButton(self.dialog_root, text='Ok', font=("", 40),
                                                   fg_color=color_cyan, hover_color=color_cyan_dark,
                                                   command=self.dialog_root_ok_button_pressed)
        self.dialog_root_ok_button.pack(side="left", padx=70, pady=25)

        self.dialog_root_cancel_button = ctk.CTkButton(self.dialog_root, text='Cancel', font=("", 40),
                                                       fg_color=color_cyan, hover_color=color_cyan_dark,
                                                       command=lambda: self.dialog_root.state("withdrawn") or
                                                       self.dialog_root.grab_release())
        self.dialog_root_cancel_button.pack(side="right", padx=70, pady=25)

        # load root
        self.load_root_is_active = 0

        # solution root
        self.solution_root_is_active = 0

        # if root.winfo_viewable() == 0:
        #   root.state(normal)
        #
        # else:
        #   root.state("withdrawn")

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
                b = 1 if self.board.count(1) == 9 else 0
                self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n" +
                                                        self.balls_counter_label.cget('text')
                                                        [len(f"Current Balls: {self.board.count(1)}\n") + b:])

        else:
            self.board.interact(y, x)
            self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                    f"Initial Balls: {self.board.count(1)}")
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
        for i, v1 in enumerate(self.board):
            for j, v2 in enumerate(v1):
                self.board_frame_list[i][j].unbind("<Button-1>")
                self.board_label_list[i][j].unbind("<Button-1>")

    def activate_board(self):
        for i, v1 in enumerate(self.board):
            for j, v2 in enumerate(v1):
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

    def rules(self):
        if self.rules_root.winfo_viewable() == 0:
            self.rules_root.state("normal")

        else:
            self.rules_root.state("withdrawn")

    def play(self):
        if self.playing:
            self.playing = 0
            self.play_setpos_button.configure(text="Play")

        else:
            if self.board.is_legal_to_start():
                self.playing = 1
                self.play_setpos_button.configure(text="Set Positon")

    def reset(self):
        if self.playing:
            self.play()

        self.game_end_root.state("withdrawn")
        self.board.reset_board()
        self.history = []
        self.history_current_place = -1
        self.update_board()
        self.balls_counter_label.configure(text="Current Balls: 0\n"
                                                "Initial Balls: 0")

    def save(self):
        self.dialog_root.state("normal")
        self.dialog_root.grab_set()

    def dialog_root_ok_button_pressed(self):
        self.save_dir_name = self.dialog_root_entry.get()

        if self.save_dir_name is not None:
            if self.is_text_legal(self.save_dir_name):
                if self.save_dir_name not in os.listdir("Saves"):
                    # self.all_exit()
                    self.root.after(170, lambda: self.save_data(self.save_dir_name))
                    self.history_current_place = -1
                    self.history = []
                    self.dialog_root.state("withdrawn")
                    self.dialog_root.grab_release()

                else:
                    self.dialog_root_label.configure(text=self.save_text2)

            else:
                self.dialog_root_label.configure(text=self.save_text3)

        else:
            self.dialog_root.state("withdrawn")
            self.dialog_root.grab_release()

    def all_exit(self):
        exits = (self.rules_exit, self.win_exit, self.load_exit, self.solution_exit)

        for exit_func in exits:
            try:
                exit_func()

            except:
                pass

    def is_text_legal(self, text):
        if len(text) > 0:
            if not text[0].isdigit():
                if "".join([y for y in text if y not in self.blocked]) == text:
                    return 1

        return 0

    def save_data(self, text):
        dir_name = f"Saves\\{text}\\"
        os.mkdir(dir_name)

        with open(f"{dir_name}{text}.dat", 'wb') as f:
            x, y = self.game_frame.winfo_rootx(), self.game_frame.winfo_rooty()
            w, h = self.game_frame.winfo_width(), self.game_frame.winfo_height()
            img = pyautogui.screenshot(region=(x, y, w, h))
            img.save(f"{dir_name}{text}.jpg")
            pickle.dump(self.board, f)

    def load(self):
        if self.load_root_is_active == 0:
            self.list_of_saves = humansorted(os.listdir("Saves"))
            self.load_folder_name = "a"
            self.current_load_save_page = 1

            self.load_root_is_active = 1
            self.load_root = ctk.CTkToplevel()
            self.load_root.title(title)
            self.load_root.after(201, lambda: self.load_root.iconbitmap(logo_path))
            self.load_root.attributes('-topmost', True)
            self.load_root.geometry(f"{800}x{550}-{0}+{0}")
            self.load_root.resizable(False, False)
            self.load_root.protocol("WM_DELETE_WINDOW", self.load_exit)

            self.load_root_main_frame = ctk.CTkFrame(self.load_root, fg_color="transparent")
            self.load_root_main_frame.pack()

            self.load_root_label = ctk.CTkLabel(self.load_root_main_frame, text="Load saves", font=("", 60),
                                                text_color=color_orange)
            self.load_root_label.pack(pady=20)

            self.load_root_saves_frame_1 = ctk.CTkFrame(self.load_root_main_frame, fg_color="transparent")
            self.load_root_saves_frame_1.pack()
            self.show_load_saves_page()

            self.load_root_load_button = ctk.CTkButton(self.load_root_main_frame, text='Load', font=("", 40),
                                                       fg_color=color_cyan, hover_color=color_cyan_dark, width=200,
                                                       command=lambda: self.confirm_flavour_strvar.set("load") or
                                                       self.confirm("load"))
            self.load_root_load_button.pack(side="left", padx=70, pady=30)

            self.load_root_delete_button = ctk.CTkButton(self.load_root_main_frame, text='Delete', font=("", 40),
                                                         fg_color=color_cyan, hover_color=color_cyan_dark, width=200,
                                                         command=lambda: self.confirm_flavour_strvar.set("delete") or
                                                         self.confirm("delete"))
            self.load_root_delete_button.pack(side="right", padx=70, pady=30)

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

        self.load_strvar = ctk.StringVar()
        self.save_frame_list = []
        self.save_image_list = []
        self.save_image_label_list = []
        self.save_radiobutton_list = []

        for i, save in enumerate(self.list_of_saves):
            save_frame = ctk.CTkFrame(self.load_root_saves_frame_2, fg_color="transparent")
            self.save_frame_list.append(save_frame)
            save_frame.bind("<Button-1>", lambda e, name=i: self.save_chosen_other(name))
            save_frame.bind("<MouseWheel>", self.save_mouse_wheel)
            save_frame.pack(side="left", padx=30 * (i % 2))

            save_image = ctk.CTkImage(dark_image=Image.open(f"Saves\\{save}\\{save}.jpg"), size=(210, 210))
            self.save_image_list.append(save_image)
            save_image_label = ctk.CTkLabel(save_frame, text=None, image=save_image)
            self.save_image_label_list.append(save_image_label)
            save_image_label.bind("<Button-1>", lambda e, name=i: self.save_chosen_other(name))
            save_image_label.bind("<MouseWheel>", self.save_mouse_wheel)
            save_image_label.pack()

            save_radiobutton = ctk.CTkRadioButton(save_frame, text=save, variable=self.load_strvar, value=save,
                                                  command=self.save_chosen_radiobutton, font=("", 30),
                                                  text_color=color_orange, hover_color=color_cyan_dark,
                                                  fg_color=color_cyan, radiobutton_width=25, radiobutton_height=25,
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
        with open(f"Saves\\{self.load_folder_name}\\{self.load_folder_name}.dat", "rb") as f:
            self.board = pickle.load(f)

        self.update_board()
        self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                f"Initial Balls: {self.board.count(1)}")

    def delete_board(self):
        os.remove(f"Saves\\{self.load_folder_name}\\{self.load_folder_name}.dat")
        os.remove(f"Saves\\{self.load_folder_name}\\{self.load_folder_name}.jpg")
        os.rmdir(f"Saves\\{self.load_folder_name}")
        self.list_of_saves = humansorted(os.listdir("Saves"))
        self.load_folder_name = None
        self.show_load_saves_page()

    def load_exit(self):
        self.load_root_is_active = 0
        self.load_root.destroy()
        self.load_folder_name = None

    def confirm(self, flavour):
        if self.load_folder_name is not None or flavour not in ["load", "delete"]:
            self.confirm_root.state("normal")
            self.confirm_root.grab_set()

    def confirm_root_yes_button_pressed(self):
        self.confirm_root.state("withdrawn")

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
        if self.solution_root_is_active == 1:
            self.solution_root.destroy()

        self.solution_root_is_active = 1
        self.solution_root = ctk.CTkToplevel()
        self.solution_root.title(title)
        self.solution_root.after(201, lambda: self.solution_root.iconbitmap(logo_path))
        self.solution_root.attributes('-topmost', True)
        self.solution_root.geometry(f"{750}x{380}-{0}+{0}")
        self.solution_root.resizable(False, False)
        self.solution_root.protocol("WM_DELETE_WINDOW", self.solution_exit)

        self.solution_main_frame = ctk.CTkFrame(self.solution_root, fg_color="transparent")
        self.solution_main_frame.pack()

        self.name_solution_label = ctk.CTkLabel(self.solution_main_frame, text="Solution",
                                                text_color=color_orange, font=("", 60))
        self.name_solution_label.pack()

        text = ""
        moves = list(enumerate(translate_moves(self.board.solution())))
        if moves:
            size = 30
            for i, move in moves:
                text += f"{i + 1}. {move}, "
                if (i + 1) % 5 == 0:
                    text += "\n"

        else:
            size = 50
            text = "None"

        self.solution_label = ctk.CTkLabel(self.solution_main_frame, text_color=color_cyan, font=("", size),
                                           text=text)
        self.solution_label.pack(pady=10)

        # if root.winfo_viewable() == 0:
        #   root.state(normal)
        #
        # else:
        #   root.state("withdrawn")

    def solution_exit(self):
        self.solution_root_is_active = 0
        self.solution_root.destroy()

    def __solve_helper(self):
        self.inactivate_board()

        for move in self.board_solution:
            t.sleep(1)
            self.board.move(move)
            self.history_tracker("move", move)
            self.update_board()
            b = 1 if self.board.count(1) == 9 else 0
            self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n" +
                                                    self.balls_counter_label.cget('text')
                                                    [len(f"Current Balls: {self.board.count(1)}\n") + b:])

        self.solve_button.configure(state="enabled")
        self.play_setpos_button.configure(state="enabled")
        self.reset_pos_button.configure(state="enabled")
        self.save_button.configure(state="enabled")
        self.load_button.configure(state="enabled")
        self.solution_button.configure(state="enabled")
        self.undo_button.configure(state="enabled")
        self.redo_button.configure(state="enabled")
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.play()
        self.activate_board()
        self.game_end()

    def solve(self):
        self.solve_button.configure(state="disabled")
        self.play_setpos_button.configure(state="disabled")
        self.reset_pos_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.load_button.configure(state="disabled")
        self.solution_button.configure(state="disabled")
        self.undo_button.configure(state="disabled")
        self.redo_button.configure(state="disabled")
        self.root.bind("<Control-y>", lambda e: 1 == 1)
        self.root.bind("<Control-z>", lambda e: 1 == 1)
        self.board_solution = self.board.solution()
        thread = th.Thread(name="Solve_Thread", target=self.__solve_helper)
        thread.start()

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
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                            f"Initial Balls: {self.board.count(1)}")

            elif self.history[self.history_current_place][0] == "M":
                move = self.history[self.history_current_place][1]
                (_, _), (y2, x2), (_, _) = process_move(move)
                self.board.interact(y2, x2)
                self.board.move(move[::-1])
                self.board.interact(y2, x2)
                self.history_current_place -= 1
                if self.playing == 1:
                    b = 1 if self.board.count(1) == 10 else 0
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n" +
                                                            self.balls_counter_label.cget('text')
                                                            [len(f"Current Balls: {self.board.count(1)}\n") - b:])

                else:
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                            f"Initial Balls: {self.board.count(1)}")

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
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                            f"Initial Balls: {self.board.count(1)}")

            elif self.history[self.history_current_place + 1][0] == "M":
                move = self.history[self.history_current_place + 1][1]
                self.board.move(move)
                self.history_current_place += 1
                if self.playing == 1:
                    b = 1 if self.board.count(1) == 9 else 0
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n" +
                                                            self.balls_counter_label.cget('text')
                                                            [len(f"Current Balls: {self.board.count(1)}\n") + b:])

                else:
                    self.balls_counter_label.configure(text=f"Current Balls: {self.board.count(1)}\n"
                                                            f"Initial Balls: {self.board.count(1)}")

            self.update_board()

        t.sleep(0.5)

    def redo(self):
        thread = th.Thread(name="Redo_Thread", target=self.__redo_helper)
        thread.start()

    def withdraw(self):
        self.rules_root.state("withdrawn")
        self.game_end_root.state("withdrawn")
        self.confirm_root.state("withdrawn")
        self.dialog_root.state("withdrawn")

    def run(self):
        self.root.after(201, self.withdraw)
        self.root.mainloop()


app = App()
app.run()

# 770
