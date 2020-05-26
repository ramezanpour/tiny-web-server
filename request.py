class Request:
    def __init__(self, raw_data):
        self.data = raw_data.decode('utf-8').split('\r\n')

    def __get_request_value(self, key: str) -> str:
        key = key.lower()
        for item in self.data[: -1]:
            splitted = item.split(':')
            if splitted[0].lower() == key:
                return splitted[1].strip()
        return ''

    @property
    def method(self) -> str:
        return str(self.data[0]).split(' ')[0]

    @property
    def http_version(self) -> str:
        return str(self.data[0]).split(' ')[2]

    @property
    def url(self) -> str:
        return str(self.data[0]).split(' ')[1]

    @property
    def user_agent(self) -> str:
        return self.__get_request_value('User-Agent')

    @property
    def accept(self) -> str:
        return self.__get_request_value('Accept')

    @property
    def content_type(self) -> str:
        return self.__get_request_value('Content-Type')

    @property
    def content_length(self) -> int:
        return self.__get_request_value('Content-Length')

    @property
    def payload(self):
        return str(self.data[-1])
