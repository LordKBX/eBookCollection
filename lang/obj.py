import locale


class Dictionary:
    def __init__(self, data: dict):
        self.data = data
        self.language = locale.getdefaultlocale()[0]

    def __getitem__(self, value: str):
        """
        get an item from storage data

        :param value: index
        :return: str|None
        """
        if value not in self.data:
            return None
        else:
            return self.data[value]
