import os
import time
import platform
from datetime import timedelta

try:
    import psutil
except ImportError:
    psutil = None

from cloudbot import hook
from cloudbot.util.filesize import size as format_bytes
import cloudbot


@hook.command("about", "version", autohelp=False)
def about(text, conn):
    """-- Gives information about CloudBot. Use .about license for licensing information"""
    if text.lower() in ("license", "gpl", "source"):
        return "CloudBot Refresh is released under the GPL v3 license, get the source code " \
               "at https://github.com/valesi/CloudBot/"

    return "{} is powered by CloudBot Refresh! ({}) - " \
           "https://github.com/valesi/CloudBot/".format(conn.nick, cloudbot.__version__)


@hook.command(autohelp=False)
def system(reply, message):
    """-- Retrieves information about the host system."""

    # Get general system info
    sys_os = platform.platform()
    python_implementation = platform.python_implementation()
    python_version = platform.python_version()
    sys_architecture = '-'.join(platform.architecture())
    sys_cpu_count = platform.machine()

    reply(
        "[h1]OS:[/h1] {} [div] "
        "[h1]Python:[/h1] {} {} [div] "
        "[h1]Architecture:[/h1] {} ({})"
        .format(
            sys_os,
            python_implementation,
            python_version,
            sys_architecture,
            sys_cpu_count)
    )

    if psutil:
        process = psutil.Process(os.getpid())

        # get the data we need using the Process we got
        cpu_usage = process.cpu_percent(1)
        thread_count = process.num_threads()
        memory_usage = format_bytes(process.memory_info()[0])
        uptime = timedelta(seconds=round(time.time() - process.create_time()))

        message(
            "[h1]Uptime:[/h1] {} [div] "
            "[h1]Threads:[/h1] {} [div] "
            "[h1]CPU Usage:[/h1] {} [div] "
            "[h1]Memory Usage:[/h1] {}"
            .format(
                uptime,
                thread_count,
                cpu_usage,
                memory_usage)
        )


@hook.command("sauce", "source", autohelp=False)
def sauce():
    """Returns a link to the source"""
    return "Check out my source code! I am a fork of cloudbot: " \
           "https://github.com/edwardslabs/CloudBot/ and my source is here: " \
           "https://github.com/valesi/CloudBot"
