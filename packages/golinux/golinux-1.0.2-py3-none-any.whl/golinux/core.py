import os
import platform
import locale
from typing import Optional

def get_system_language() -> str:
    """Определяет язык системы"""
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            return lang.lower()
    except:
        pass
    return 'en'  # По умолчанию английский

def _get_localized_message(lang: str) -> dict:
    """Возвращает локализованные строки для разных языков"""
    messages = {
        'ru': {
            'warning': "ВНИМАНИЕ! Вы используете Windows - закрытую и антиконфидециальную ОС!",
            'data': "Ваши данные принадлежат не только вам, ими управляет Microsoft!",
            'switch': "Переходите на Linux - систему СВОБОДЫ, БЕЗОПАСНОСТИ и КОНТРОЛЯ!",
            'tags': "#WindowsIsSpyware           #GoLinux         #FreeYourComputer",
            'install': ">>> Установите Linux сегодня: https://www.pureos.net/download/ <<<",
            'ps1': "P.S Этот скрипт не гарантирует нормальную",
            'ps2': "работу на Windows, поддержка ограничена",
            'no_color': "#GoLinux Ваша ОС собирает данные о вас, рекомендуем Linux"
        },
        'en': {
            'warning': "WARNING! You are using Windows - a closed and anti-privacy OS!",
            'data': "Your data is not fully yours - Microsoft controls it!",
            'switch': "Switch to Linux - a system of FREEDOM, SECURITY and CONTROL!",
            'tags': "#WindowsIsSpyware           #GoLinux         #FreeYourComputer",
            'install': ">>> Install Linux today: https://www.pureos.net/download/ <<<",
            'ps1': "P.S This script does not guarantee normal",
            'ps2': "operation on Windows, support is limited",
            'no_color': "#GoLinux Your OS collects your data, we recommend Linux"
        },
        'es': {
            'warning': "¡ATENCIÓN! Estás usando Windows, un sistema cerrado y sin privacidad.",
            'data': "¡Tus datos no son solo tuyos, Microsoft los controla!",
            'switch': "¡Cambia a Linux - un sistema de LIBERTAD, SEGURIDAD y CONTROL!",
            'tags': "#WindowsEsEspía           #GoLinux         #LiberaTuPC",
            'install': ">>> Instala Linux hoy: https://www.pureos.net/download/ <<<",
            'ps1': "P.D. Este script no garantiza un funcionamiento",
            'ps2': "normal en Windows, el soporte es limitado",
            'no_color': "#UsaLinux Tu sistema recopila tus datos, te recomendamos Linux"
        },
        'fr': {
            'warning': "ATTENTION ! Vous utilisez Windows - un système fermé et anti-vie privée !",
            'data': "Vos données ne vous appartiennent pas entièrement, Microsoft les contrôle!",
            'switch': "Passez à Linux - un système de LIBERTÉ, SÉCURITÉ et CONTRÔLE !",
            'tags': "#WindowsEstEspion         #GoLinux      #LibérezVotrePC",
            'install': ">>> Installez Linux: https://www.pureos.net/download/ <<<",
            'ps1': "P.S Ce script ne garantit pas un fonctionnement",
            'ps2': "normal sous Windows, le support est limité",
            'no_color': "#PassezÀLinux Votre OS collecte vos données, nous recommandons Linux"
        },
        'de': {
            'warning': "WARNUNG! Sie nutzen Windows - ein geschlossenes, datenschutzfeindliches OS!",
            'data': "Ihre Daten gehören nicht nur Ihnen - Microsoft kontrolliert sie!",
            'switch': "Wechseln Sie zu Linux - ein System für FREIHEIT, SICHERHEIT und KONTROLLE!",
            'tags': "#WindowsIstSpionage      #GoLinux    #BefreitEurenPC",
            'install': ">>> Installieren Sie Linux: https://www.pureos.net/download/ <<<",
            'ps1': "P.S Dieses Script garantiert keine normale",
            'ps2': "Funktion unter Windows, der Support ist begrenzt",
            'no_color': "#WechseltZuLinux Ihr OS sammelt Ihre Daten, wir empfehlen Linux"
        },
        'zh': {
            'warning': "警告！您正在使用Windows——一个封闭且侵犯隐私的操作系统！",
            'data': "您的数据不完全属于您，微软在控制它！",
            'switch': "转向Linux——一个自由、安全和可控的系统！",
            'tags': "#Windows是间谍软件      #GoLinux        #解放你的电脑",
            'install': ">>> 立即安装Linux: https://www.pureos.net/download/ <<<",
            'ps1': "注：本脚本不保证在Windows上正常运行，支持有限。",
            'ps2': "",
            'no_color': "#改用Linux 您的系统在收集数据，我们推荐Linux"
        }
    }
    
    # Возвращаем сообщения для указанного языка или английский по умолчанию
    return messages.get(lang.split('_')[0], messages['en'])

def _windows_propaganda() -> None:
    """Выводит пропаганду Linux на Windows с учетом языка системы"""
    lang = get_system_language()
    msg = _get_localized_message(lang)
    
    try:
        from colorama import Fore, Style, init
        init()
        border = Fore.RED + Style.BRIGHT
        text = Fore.YELLOW + Style.BRIGHT
        warning = Fore.RED + Style.BRIGHT
        reset = Style.RESET_ALL
        light_grey = Style.BRIGHT + Fore.BLACK
        
        # ASCII арт
        print(border + " _____          _      _                     " + reset)
        print(border + "|  __ \        | |    (_)                    " + reset)
        print(border + "| |  \/  ___   | |     _  _ __   _   _ __  __" + reset)
        print(border + "| | __  / _ \  | |    | || '_ \ | | | |\ \/ /" + reset)
        print(border + "| |_\ \| (_) | | |____| || | | || |_| | >  < " + reset)
        print(border + r" \____/ \___/  \_____/|_||_| |_| \__,_|/_/\_\\" + reset)
        print()
        
        # Верхняя граница
        print(warning + "  ╔════════════════════════════════════════════════════════════════════════════╗" + reset)
        
        # Строки текста (ровно 80 символов между границами)
        print(warning + "  ║" + text + msg['warning'].center(76) + warning + "║" + reset)
        print(warning + "  ║" + text + msg['data'].center(76) + warning + "║" + reset)
        print(warning + "  ║" + text + msg['switch'].center(76) + warning + "║" + reset)
        print(warning + "  ║" + " " * 76 + warning + "║" + reset)  # Пустая строка
        
        # Хэштеги и ссылка
        print(warning + "  ║" + text + msg['tags'].center(76) + warning + "║" + reset)
        print(warning + "  ║" + Fore.CYAN + Style.BRIGHT + msg['install'].center(76) + warning + "║" + reset)
        
        # Примечание
        if msg['ps1']:
            print(warning + "  ║" + light_grey + msg['ps1'].center(76) + warning + "║" + reset)
        if msg['ps2']:
            print(warning + "  ║" + light_grey + msg['ps2'].center(76) + warning + "║" + reset)
        
        # Нижняя граница
        print(warning + "  ╚════════════════════════════════════════════════════════════════════════════╝" + reset)
    
    except ImportError:
        print(msg['no_color'])
        print("\n" + _get_localized_message('en')['no_color'] + "\nTip: Install colorama for colored output: pip install colorama")



    

def check_os(silent: bool = False, env_flag: Optional[str] = "GoLinuxFlag") -> bool:
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