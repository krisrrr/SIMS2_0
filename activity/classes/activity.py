class ActivityEntity:
    def __init__(self, t, c, i, s, h):
        self.timestamp = t
        self.category = c
        self.intensity = i
        self.steps = s
        self.heart_rate = h
    
    def __str__(self):
        return "{}: category: {}; intensity {}; steps {}; heart rate {};".format(
            self.timestamp.strftime('%d.%m - %H:%M'), 
            self.category, 
            self.intensity,
            self.steps, 
            self.heart_rate
        )