"""
Housie AI — Cross-Platform Computer Control Layer
"""
from .base import BaseController
from .factory import get_controller
from .windows import WindowsController
from .macos import MacOSController
from .linux import LinuxController
from .android import AndroidController
