class Toggle:
    def __init__(self):
        self.last_id = ''
        self.bg_color = False

    def toggle_by_tag(self, key, show_value):
        if self.last_id == '':
            self.last_id = key
            return show_value, False
        if key == self.last_id:
            self.last_id = key
            return '', True
        else:
            self.last_id = key
            return show_value, False
