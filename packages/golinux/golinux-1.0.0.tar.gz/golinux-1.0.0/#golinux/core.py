# propaganda_linux.py
import os
import platform
from typing import Optional

def _windows_propaganda() -> None:
    """Выводит пропаганду Linux на Windows"""
    try:
        from colorama import Fore, Style, init
        init()  # Инициализация colorama для Windows
        border = Fore.RED
        text = Fore.YELLOW
        reset = Style.RESET_ALL
        
        print(border + "╔════════════════════════════════════════════════╗" + reset)
        print(border + "║" + text + "               WE NOT SUPPORT WINDOWS!          " + border + "║" + reset)
        print(border + "║" + text + "                  #GoLinux                       " + border + "║" + reset)
        print(border + "╚════════════════════════════════════════════════╝" + reset)
    except ImportError:
        # Если colorama не установлена, выводим без цветов
        print("╔════════════════════════════════════════════════╗")
        print("║               WE NOT SUPPORT WINDOWS!          ║")
        print("║                  #GoLinux                       ║")
        print("╚════════════════════════════════════════════════╝")
        print("Установите colorama для цветного вывода: pip install colorama")

def check_os(silent: bool = False, env_flag: Optional[str] = "MY_FLAG") -> bool:
    """
    Проверяет ОС и выводит сообщение, если это Windows.
    
    Args:
        silent: Если True, не выводит сообщение
        env_flag: Имя переменной окружения, которая отключает пропаганду
        
    Returns:
        bool: True если ОС не Windows или установлена переменная окружения
    """
    if platform.system() == "Windows":
        if os.getenv(env_flag) is None and not silent:
            _windows_propaganda()
        return False
    return True

# Автоматически проверяем при импорте
check_os()