import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox

entities = []
user_number = 0


class Start_Window(tk.Frame):
    '''login window'''
    attempts = 0

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        top = self.top = master
        top.title('Input Pasword')
        top.geometry('{}x{}'.format(350, 100))
        top.resizable(width=False, height=False)

        self.top.protocol('WM_DELETE_WINDOW', self.on_exit)

        self.l_login = tk.Label(top, text='Login: ', font=(
            'Courier', 10), justify=tk.LEFT)
        self.l_login.grid(row=0, column=0, padx=10, pady=5)

        self.l_password = tk.Label(top, text='Password: ', font=(
            'Courier', 10), justify=tk.LEFT)
        self.l_password.grid(row=0, column=1, padx=10, pady=5)

        self.e_login = tk.Entry(top, width=25)
        self.e_login.grid(row=1, column=0, padx=10, pady=5)

        self.e_password = tk.Entry(top, show='*', width=25)
        self.e_password.grid(row=1, column=1, padx=10, pady=5)

        self.b_log = tk.Button(top, text='Login',
                               command=self.cleanup, font=('Courier, 12'))
        self.b_log.grid(row=2, column=0, padx=10, pady=5)

        self.b_reg = tk.Button(top, text='Register',
                               command=self.register, font=('Courier, 12'))
        self.b_reg.grid(row=2, column=1, padx=10, pady=5)

    def cleanup(self):
        '''checks if given login and password are valid and if, opens actual aplication, also counts attempts and closes aplication if attempts ==5'''
        self.value_log = self.e_login.get()
        self.value_pas = self.e_password.get()
        access = read_file('users.txt')
        for i in range(len(access)):
            access[i][0] = decrypt(access[i][0])
            access[i][1] = decrypt(access[i][1])
        if any([i[0] == self.value_log and i[1] == self.value_pas for i in access]):
            self.e_login.delete(0, 'end')
            self.e_password.delete(0, 'end')
            self.top.withdraw()
            Main_window(self.top, self.value_log, self.value_pas)

        else:
            self.attempts += 1
            if self.attempts == 5:
                root.quit()
            self.e_login.delete(0, 'end')
            self.e_password.delete(0, 'end')
            tk.messagebox.showerror(
                'Incorrect Password', 'Incorrect pasword, attempts ramaining: ' + str(5-self.attempts))

    def register(self):
        '''Opens Registration window'''
        Register_win(self.top)

    def on_exit(self):
        '''closes app'''
        if tk.messagebox.askyesno('Exit', 'Do you want ot quit?'):
            root.destroy()


class Register_win(object):
    '''Window responsible for meking registration possible'''

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.title('Register')
        top.geometry('335x100')
        top.resizable(width=False, height=False)
        top.protocol('WM_DELETE_WINDOW', self.on_exit)
        top.grab_set()
        top.focus_set()

        self.file_read = read_file('users.txt')
        self.file = open('users.txt', 'a')

        self.l_log = tk.Label(top, text='Login: ', font=(
            'Courier, 10'), justify=tk.LEFT)
        self.l_log.grid(row=0, column=0)

        self.l_pas = tk.Label(top, text='Password: ',
                              font=('Courier, 10'), justify=tk.LEFT)
        self.l_pas.grid(row=1, column=0)

        self.l_pas_rep = tk.Label(
            top, text='Repeat Password: ', font=('Courier, 10'), justify=tk.LEFT)
        self.l_pas_rep.grid(row=2, column=0, padx=5)

        self.e_log = tk.Entry(top, width=25)
        self.e_log.grid(row=0, column=1)

        self.e_pas = tk.Entry(top, show='*', width=25)
        self.e_pas.grid(row=1, column=1)

        self.e_pas_rep = tk.Entry(top, show='*', width=25)
        self.e_pas_rep.grid(row=2, column=1)

        self.b_ok = tk.Button(top, text='Accept',
                              command=self.save, font=('Courier, 11'))
        self.b_ok.grid(row=3, column=0)

    def save(self):
        '''saves new user to file containing all users and creates personal file for this specific user'''
        global user_number
        if self.check_valid() == True:
            self.file.writelines(self.val_log + ',' + self.val_pas + ',\n')
            file = open(
                'user' + str(user_number) + '.txt', 'w')
            user_number += 1
            file.close()
            if tk.messagebox.showinfo(parent=self.top, title='Succesful', message='You have been registered'):
                self.file.close()
                self.top.destroy()

    def check_valid(self):
        '''Checks if given data is valid'''
        self.val_log = self.e_log.get()
        self.val_pas = self.e_pas.get()
        self.val_pas_rep = self.e_pas_rep.get()
        self.val_log, self.val_pas, self.val_pas_rep = encrypt(
            self.val_log), encrypt(self.val_pas), encrypt(self.val_pas_rep)

        if self.val_pas != self.val_pas_rep:
            self.e_pas.delete(0, 'end')
            self.e_pas_rep.delete(0, 'end')
            tk.messagebox.showerror(
                parent=self.top, title='Error', message='Passwords dont not match')
            return False

        elif self.val_log == self.val_pas:
            self.clear_entrys()
            tk.messagebox.showerror(
                parent=self.top, title='Error', message='Login cant be the same as password')
            return False
        elif any([i[0] == self.val_log or i[1] == self.val_pas for i in self.file_read]):
            self.clear_entrys()
            tk.messagebox.showerror(parent=self.top,
                                    title='Error', message='Login or password already in use')
            return False

        elif any([i == ' ' for i in self.val_log or j == ' ' for j in self.val_pas]):
            self.clear_entrys()
            tk.messagebox.showerror(parent=self.top,
                                    title='Error', message="Login or password contains ' '")
            return False
        else:
            return True

    def clear_entrys(self):
        '''Clears all entries'''
        self.e_log.delete(0, 'end')
        self.e_pas.delete(0, 'end')
        self.e_pas_rep.delete(0, 'end')

    def on_exit(self):
        self.file.close()
        self.top.destroy()


class Main_window(object):
    '''Main window of aplication managing data saved by logged user'''

    def __init__(self, master, login, password):
        top = self.top = tk.Toplevel(master)
        top.title('Data holder')
        top.resizable(width=False, height=False)
        top.protocol('WM_DELETE_WINDOW', master.destroy)
        top.grab_set()
        top.focus_set()
        top.grid_columnconfigure(3, weight=1)

        self.master = master
        self.login = login
        self.password = password

        self.l_welcome = tk.Label(top, text='Welcome', font=(
            'Courier, 14'), justify=tk.CENTER)
        self.l_welcome.grid(row=0, columnspan=4, sticky='n')

        self.l_name = tk.Label(
            top, text='Name: ', font=('Courier, 10'), justify=tk.LEFT)
        self.l_name.grid(row=1, column=0, sticky='w')

        self.l_login = tk.Label(top, text='Login: ', font=(
            'Courier, 10'), justify=tk.LEFT)
        self.l_login.grid(row=2, column=0, sticky='w')

        self.l_password = tk.Label(
            top, text='Password: ', font=('Courier, 10'), justify=tk.LEFT)
        self.l_password.grid(row=3, column=0, sticky='w')

        self.l_data_saved = tk.Label(
            top, text='Data saved : ', font=('Courier, 10'), justify=tk.LEFT)
        self.l_data_saved.grid(row=5, columnspan=3, sticky='w')

        self.l_saved_name = tk.Label(top, text='Name: ', font=('Courier, 10'))
        self.l_saved_name.grid(row=6, column=0)

        self.l_saved_log = tk.Label(top, text='login: ', font=('Courier, 10'))
        self.l_saved_log.grid(row=6, column=1, padx=50)

        self.l_saved_pas = tk.Label(
            top, text='Password: ', font=('Courier, 10'))
        self.l_saved_pas.grid(row=6, column=2, sticky='e',)

        self.e_name = tk.Entry(top, width=40)
        self.e_name.grid(row=1, column=1, columnspan=3, padx=10)

        self.e_log = tk.Entry(top, width=40)
        self.e_log.grid(row=2, column=1, columnspan=3, padx=10)

        self.e_pas = tk.Entry(top, width=40)
        self.e_pas.grid(row=3, column=1, columnspan=3, padx=10)

        self.b_save = tk.Button(
            top, text='Save', command=self.save, font=('Courier, 10'))
        self.b_save.grid(row=4, column=0, padx=10)

        self.b_log_out = tk.Button(top, text='Log Out', font=(
            'Courier, 10'), command=self.log_out)
        self.b_log_out.grid(row=4, column=3, padx=10)

        self.load_file(
            self.top, 'user'+str(check_wchich_user(self.login, self.password)) + '.txt')

    def log_out(self):
        '''Makes login window visible again and closes main window'''
        for ent in entities:
            ent.destroy()
        entities.clear()
        self.master.deiconify()
        self.top.destroy()

    def load_file(self, top, file_name):
        '''loads previously saved data from user's file'''
        temp = read_file(file_name)
        for i in range(len(temp)):
            entities.append(Display_entity(
                top, decrypt(temp[i][1]), decrypt(temp[i][2]), decrypt(temp[i][0]), len(entities), self.login, self.password))
        for ent in entities:
            ent.render()

    def save(self):
        '''Saves given data to user's file'''
        name = self.e_name.get()
        login = self.e_log.get()
        password = self.e_pas.get()
        file = open('user'+str(check_wchich_user(self.login,
                                                 self.password))+'.txt', 'a')
        file.writelines(encrypt(
            name) + ',' + encrypt(login) + ',' + encrypt(password) + ',\n')

        self.e_name.delete(0, 'end')
        self.e_log.delete(0, 'end')
        self.e_pas.delete(0, 'end')
        if tk.messagebox.showinfo(parent=self.master, title='Added Succesfully', message='Entity added succesfully,\n' + 'Name: ' + name + '\nLogin: ' + login + '\nPassword: '+password):
            entities.append(Display_entity(
                self.top, login, password, name, len(entities), self.login, self.password))
            for ent in entities:
                ent.render()


class Display_entity():
    '''Class representing single display of saved data on a mainn window'''

    def __init__(self, master, login, password, name, ent_num, master_login, master_pasword):
        self.master = master
        self.login = login
        self.password = password
        self.name = name
        self.ent_num = ent_num
        self.master_log = master_login
        self.master_pas = master_pasword

        self.l_login = tk.Label(
            self.master, text=self.login, font=('Courier, 10'))
        self.l_password = tk.Label(
            self.master, text=self.password, font=('Courier, 10'))
        self.l_name = tk.Label(
            self.master, text=self.name, font=('Courier, 10'))

        self.b_delete = tk.Button(
            self.master, command=self.delete, text='X', font=('Courier, 7'))

    def render(self):
        '''Renders/Rerenders instance of data on main window'''
        self.l_name.grid(row=7 + self.ent_num, column=0)
        self.l_login.grid(row=7 + self.ent_num, column=1)
        self.l_password.grid(row=7 + self.ent_num, column=2)
        self.b_delete.grid(row=7 + self.ent_num, column=3, sticky='e')

    def destroy(self):
        '''Destroys all labels and buttons'''
        self.l_login.destroy()
        self.l_name.destroy()
        self.l_password.destroy()
        self.b_delete.destroy()

    def delete(self):
        '''Deletes instance of saved data from screen and user's file'''
        if tk.messagebox.askyesno(parent=self.master, title='Delete', message='Are you sure you want to delete this entry?'):
            self.destroy()
            for i in range(len(entities)):
                if entities[i] == self:
                    for j in range(i, len(entities)):
                        entities[j].ent_num -= 1
                    entities.pop(i)
                    self.delete_from_file()
                    break

    def delete_from_file(self):
        '''Method responsible for deleting data from user's file'''
        file = open(
            'user'+str(check_wchich_user(self.master_log, self.master_pas))+'.txt', 'r')
        lines = file.readlines()
        file.close()
        file = open(
            'user'+str(check_wchich_user(self.master_log, self.master_pas))+'.txt', 'w')
        for l in lines:
            if l.strip('\n') != encrypt(str(self.name)) + ',' + encrypt(str(self.login)) + ',' + encrypt(str(self.password)) + ',':
                file.writelines(l)
        file.close()


def read_file(file_name):
    '''Reads given file separating lines instances'''
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()
    temp = []
    for i in lines:
        temp.append(i.split(','))
    return temp


def decrypt(val):
    '''Decrypts given value'''
    decrypt = ''
    for i in val:
        decrypt += chr(ord(i)-5)
    return decrypt


def encrypt(val):
    '''Encrypts given value'''
    encrypt = ''
    for i in val:
        encrypt += chr(ord(i)+5)
    return encrypt


def check_wchich_user(login, password):
    '''Checks which user is curentrly logged'''
    temp = read_file('users.txt')
    for i in range(len(temp)):
        if temp[i][0] == encrypt(login) and temp[i][1] == encrypt(password):
            return i


if __name__ == "__main__":
    root = tk.Tk()
    Start_Window(root).grid()
    root.mainloop()
