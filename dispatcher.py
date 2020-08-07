import os
import win32file
import win32con
import smtp_sender
import datetime

ACTIONS = {
    1: "Создан",
    2: "Удалён",
    3: "Изменён"
}
FILE_LIST_DIRECTORY = 0x0001

MESSAGE_LIST = []
SENDNOW = False
TIMEOUT = 1  # min
TIME = 0
TIMENOW = 0


def set_mailing_interval(interval):
    global TIMEOUT
    r = 1
    try:
        r = int(interval)
        print("USING ", r, " min INTERVAL!")
    except:
        r = 1
        print("USING DEFAULT INTERVAL (1min)!")
    finally:
        TIMEOUT = r


def start_dispatching(path_to_watch, t):
    global SENDNOW, TIMENOW
    TIMENOW = datetime.datetime.now()
    MESSAGE_LIST.clear()

    hDir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while getattr(t, "do_disp", True):
        results = win32file.ReadDirectoryChangesW(  # считываем изменения
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY |
            win32con.CREATE_NEW,
            None,
            None
        )
        for action, file in results:
            full_filename = os.path.join(path_to_watch, file)
            act = ACTIONS.get(action, "Unknown")
            if str(full_filename).endswith(".tmp") or act == "Unknown":
                pass
            else:
                print(datetime.datetime.now(), ":::", full_filename, ":::", act)
                diff = datetime.datetime.now().__sub__(TIMENOW).seconds
                if diff > TIMEOUT * 60:
                    SENDNOW = False
                    TIMENOW = datetime.datetime.now()
                    if len(MESSAGE_LIST) > 0:
                        print(datetime.datetime.now(), "...отправка собранной статистики за ", TIMEOUT, "мин")
                        smtp_sender.send_smtp_email('\n'.join(MESSAGE_LIST))
                    MESSAGE_LIST.clear()
                else:
                    MESSAGE_LIST.append(
                        datetime.datetime.now().__str__() + " ::: " + full_filename + " ::: " + ACTIONS.get(action,
                                                                                                            "Unknown"))
    MESSAGE_LIST.clear()
