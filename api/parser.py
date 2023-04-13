class ParserAPI:
    def __init__(self):
        self.parsers = {}

    def register_parser(self, file_type, parser):
        self.parsers[file_type] = parser

    def parse_file(self, file_path):
        file_type = self.get_file_type(file_path)

        if file_type not in self.parsers:
            raise ValueError(f"No parser registered for file type: {file_type}")

        parser = self.parsers[file_type]
        return parser.parse(file_path)

    @staticmethod
    def get_file_type(file_path):
        return file_path.split('.')[-1].lower()