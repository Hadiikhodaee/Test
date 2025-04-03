class Manager:
    def __init__(self, _class=None):
        self._class = _class
        
    def __str__(self):
        return f"Manager {self._class}"
    
    def count(self):
        return len(self._class.object_list)
    
    def get(self, **kwargs):
        obj_list = []
        for key, value in kwargs.items():
            for obj in self._class.object_list:
                if hasattr(obj, key) and getattr(obj, key) == value:
                    obj_list.append(obj)
                
        return obj_list