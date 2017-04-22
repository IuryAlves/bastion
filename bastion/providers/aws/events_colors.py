# coding: utf-8

from colorama import Fore


event_color_map = {
    'CREATE_COMPLETE': Fore.GREEN,
    'CREATE_FAILED': Fore.RED,
    'CREATE_IN_PROGRESS': Fore.YELLOW,
    'DELETE_COMPLETE': Fore.GREEN,
    'DELETE_FAILED': Fore.RED,
    'DELETE_IN_PROGRESS': Fore.YELLOW,
    'ROLLBACK_COMPLETE': Fore.GREEN,
    'ROLLBACK_FAILED': Fore.RED,
    'ROLLBACK_IN_PROGRESS': Fore.YELLOW,
    'UPDATE_COMPLETE': Fore.GREEN,
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': Fore.YELLOW,
    'UPDATE_IN_PROGRESS': Fore.YELLOW,
    'UPDATE_ROLLBACK_COMPLETE': Fore.GREEN,
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': Fore.YELLOW,
    'UPDATE_ROLLBACK_FAILED': Fore.RED,
    'UPDATE_ROLLBACK_IN_PROGRESS': Fore.GREEN
}
