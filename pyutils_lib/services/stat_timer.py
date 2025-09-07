from datetime       import datetime, timedelta

class StatTimer():
    """
    The StatTimer is a simple class, which allows you calculate the execution time of a block code. 

    For Example: 
        this_timer = StatTimer()
        [a bunch of code]
        log.debug(f"It took: {this_timer.Duration()}")
    """
    def __init__(self):
        self.StartTime  = datetime.now()
        self.EndTime    = None

    def Duration(self)->timedelta:
        """
        This function will return the difference between the time the object was created, and the time that this method was first called. 

        Returns:
            timedelta: the difference between the time the StatTimer was created and the time that this method was first called. 
        """
        if self.EndTime is None:
            self.EndTime = datetime.now()

        return self.EndTime - self.StartTime
    