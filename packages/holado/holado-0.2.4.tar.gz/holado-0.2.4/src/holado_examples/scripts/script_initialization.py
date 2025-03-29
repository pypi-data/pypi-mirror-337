import holado


# Minimal HolAdo initialization

import logging
logging.print("After 'import holado', HolAdo is initialized minimally with logging levels 'trace' and 'print'")


# Initialize HolAdo with default behaviours

holado.initialize(log_on_console=True, log_in_file=False)
logging.print("After 'holado.initialize(log_on_console=True, log_in_file=False)', HolAdo is initialized:")
logging.print("  - to log on console but not in file")
logging.print("  - launch garbage collector periodically (without specifying garbage_collector_periodicity, default periodicity is 10 s)")



