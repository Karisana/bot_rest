
class SendAdmin:
    """Формирует сообщение для отправки его пользователям"""

    def __init__(self):
        self.admin_dict = {'photo': '', 'text': '', 'link': ''}

    def get_img(self, photo_id):
        if len(self.admin_dict['photo']) > 2:
            self.admin_dict['photo'] = photo_id
        else:
            self.admin_dict['photo'] = photo_id

    def get_text(self, some_text):
        self.admin_dict['text'] = some_text

    def get_link(self, some_link):
        self.admin_dict['link'] = some_link

    @property
    def res_mes(self):
        return self.admin_dict
