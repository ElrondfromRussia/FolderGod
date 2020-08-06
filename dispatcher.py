import os
import win32file
import win32con
import smtp_sender

ACTIONS = {
    1: "Создан",
    2: "Удалён",
    3: "Изменён"
}
FILE_LIST_DIRECTORY = 0x0001


def start_dispatching(path_to_watch, t):
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
                print(full_filename, act)
                smtp_sender.send_smtp_email(full_filename + " ::: " + ACTIONS.get(action, "Unknown"))
