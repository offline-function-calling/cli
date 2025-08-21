import psutil

def get_system_info():
    """
    Returns detailed information about the system's CPU, RAM, and disk usage.

    This tool provides a comprehensive overview of the system's hardware resource utilization.

    Returns:
        dict: A dictionary containing detailed information about CPU, RAM, and disk usage.
    """
    # CPU Information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # Memory Information
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    # Disk Information
    disk_usage = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()

    return {
        "cpu": {
            "percent_usage": cpu_percent,
            "core_count": cpu_count,
            "current_frequency_mhz": cpu_freq.current if cpu_freq else 'N/A',
            "max_frequency_mhz": cpu_freq.max if cpu_freq else 'N/A',
        },
        "memory": {
            "virtual": {
                "total_gb": round(virtual_mem.total / (1024**3), 2),
                "available_gb": round(virtual_mem.available / (1024**3), 2),
                "percent_used": virtual_mem.percent,
            },
            "swap": {
                "total_gb": round(swap_mem.total / (1024**3), 2),
                "used_gb": round(swap_mem.used / (1024**3), 2),
                "percent_used": swap_mem.percent,
            },
        },
        "disk": {
            "total_gb": round(disk_usage.total / (1024**3), 2),
            "used_gb": round(disk_usage.used / (1024**3), 2),
            "free_gb": round(disk_usage.free / (1024**3), 2),
            "percent_used": disk_usage.percent,
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
        },
    }
