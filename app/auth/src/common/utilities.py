class Utils:
    @staticmethod
    def sanitize(input):
        # TODO: implement sanitize functionality
        return input

    @staticmethod
    def sanitize_dict(input):
        sanitized_input = dict()
        for key, val in input.items():
            sanitized_input[key] =  Utils.sanitize(input[key])
        return  sanitized_input