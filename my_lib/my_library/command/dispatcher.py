from my_lib.my_library.command.response import ok, err

class Dispatcher:
    def __init__(self, parse_line_func, commands_dict, error_mapper=None):
        self.parse_line = parse_line_func
        self.commands = commands_dict
        self.error_mapper = error_mapper

    def dispatch(self, raw_line, app):
        try:
            code, arg1, arg2 = self.parse_line(raw_line)
            cmd = self.commands.get(code)
            if not cmd:
                return err("Unknown command.")

            out_code, payload = cmd.execute(app, raw_line, arg1, arg2)

            if out_code == "RAW":
                return payload

            return ok(out_code, payload)

        except Exception as e:
            if self.error_mapper:
                mapped = self.error_mapper(e)
                if mapped:
                    return mapped
            return err("Error occurred in application.")
