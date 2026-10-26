import re

class Interpreter:
    # # Old:
    # (r'((?<!~)(?:~~)*)\$([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$)')
    # (r'((?<!~)(?:~~)*)\$`((?:[^`~]|~~|~`)*?)`')
    
    # # Update:
    # (r'(~*)\$([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$)')
    # (r'(~*)\$`((?:[^`~]|~~|~`)*?)`')
    
    # RegEx:
    (r'(~*)\$(`((?:[^`~]|~~|~`)*?)`|([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|\$|$))')
    (r'^\$([a-zA-Z_][a-zA-Z0-9_]*)$')
    (r'^\$`((?:[^`~]|~~|~`)*?)`$')

    (r"(~*)@('((?:[^'~]|~~|~')*?)'|([a-zA-Z_][a-zA-Z0-9_]>*)(?=\s|@|$))")

    pystart = '\$'
    pygroup = '`'
    objstart = "@"
    objgroup = "'"
    objsub = ">"
    escape = '\?'
    escape_ = '?'
    
    a = r'('+escape+r'*)' + pystart + r'([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|' + pystart + r'|$)'
    b = r'('+escape+r'*)' + pystart+pygroup + r'((?:[^'+pygroup+escape+r']|'+escape*2+r'|'+escape+pygroup+r')*?)' + pygroup

    pyPatternStringGrouped = pygroup + r'((?:[^'+pygroup+escape+r']|'+escape*2+r'|'+escape+pygroup+r')*?)' + pygroup
    pyPatternStringUngrouped = r'([a-zA-Z_][a-zA-Z0-9_]*)(?=\s|' + pystart + r'|'+ escape +r'|$)'
    pyPatternString = pystart + r'(' + pyPatternStringGrouped + r'|'+ pyPatternStringUngrouped + r')'

    objPatternString = r"@('((?:[^'\?]|\?\?|\?'|\?>)*?)'|([a-zA-Z0-9_>]*)(?=\s|@|$))"

    allPatternString = r'('+escape+r'*)((' + pyPatternString + r')|(' + objPatternString + r'))'

    pyPatternAnyTypeUngrouped = r'^' + pystart + r'([a-zA-Z_][a-zA-Z0-9_]*)$'
    pyPatternAnyTypeGrouped = r'^' + pystart+pygroup + r'((?:[^'+pygroup+escape+r']|'+escape*2+r'|'+escape+pygroup+r')*?)' + pygroup+r'$'

    objPatternAnyTypeUngrouped = r'^@([a-zA-Z0-9_>]*)$'
    objPatternAnyTypeGrouped = r"^@'((?:[^'\?]|\?\?|\?'|\?>)*?)'$"
    objPatternAnyType = r"^@('((?:[^'\?]|\?\?|\?'|\?>)*?)'|([a-zA-Z0-9_>]*))$"

    @staticmethod
    class unresolved:
        def __init__(self, script=None):
            self.script = script

    def __init__(self, data, refs=globals()):
        self.data = data
        self.refs = refs

        self.dataobject = {
						"data": None
                        }

        self.queue = {}
        self.resolved = []

    def process(self):
        self.interpret(self.data, "data", self.dataobject)
        self.resolve()

        return self.dataobject["data"]

    def interpret(self, value, key, container, reference=None):
        try:
            script = container[key].script
        except (KeyError, IndexError, ValueError, AttributeError): # ISSUE: Should ValueError really be considered here?
            script = Script(value, key, container, self)

            if isinstance(value, str):
                script.process()
                script.queue()
                container[key] = script.result

            elif isinstance(value, list):
                container[key] = []

                for i, v in enumerate(value):
                    container[key].append(None)
                    self.interpret(v, i, container[key])

            elif isinstance(value, dict):
                container[key] = {}

                for k, v in value.items():
                    self.interpret(v, k, container[key])

            else:
                container[key] = value
        else:
            script.resume(reference)
            script.queue()
            container[key] = script.result

        script.announceresolved()

    def resolve(self):
        i = 0
        while len(self.queue):
            reference = self.resolved[i]
            citations = self.queue[reference]

            for citation in citations:
                value, key, container = citation.ref[0], citation.ref[1], citation.ref[2]
                self.interpret(value, key, container, reference)

            del self.queue[reference]
            i += 1

class Script:
    def __init__(s, value, key, container, interpreter):
        s.ref = value, key, container
        s.i = interpreter

        s.ATForms = [
            s.pyInterpretATUG,
            s.pyInterpretATG,
            s.objInterpretAT
            ]

        s.parts = []
        s.awaiting = {}
        s.parsed = 0
        s.match = None
        s.reset()

    def reset(s):
        s.valid = True

    def process(s):
        value = s.ref[0]

        match = re.search(s.i.pyPatternAnyTypeUngrouped, value)
        if match:
            s.route(match, 0)
            return

        match = re.search(s.i.pyPatternAnyTypeGrouped, value)
        if match:
            s.route(match, 1)
            return

        match = re.search(s.i.objPatternAnyType, value)
        if match:
            s.route(match, 2)
            return

        s.multiInterpretS()

    def resume(s, reference):
        if s.match: # ISSUE: Check how match (Match object) could be None.
            s.route(s.match, s.form)
        else:
            targets = s.awaiting[reference]

            for n in targets:
                match = s.parts[n]
                result = s.interpretS(match)

                if not isinstance(result, s.i.unresolved):
                    s.parts[n] = result

            del s.awaiting[reference]
            s.reset()

            if not s.awaiting:
                s.result = "".join(s.parts) # ISSUE: Does s.interpretS return strictly string?

    def route(s, match, form):
        s.form = form
        s.ATForms[form](match)

    def pyInterpretATUG(s, match):
        s.code = match.group()
        s.expression = match.group(1)
        
        try:
            s.result = s.evaluate()
        except NameError:
            s.valid = False
            s.result = s.code

    def pyInterpretATG(s, match):
        s.code = match.group()
        s.expression = match.group(1)

        s.result = s.interpret()

    def objInterpretAT(s, match):
        s.code = match.group()
        s.expression = match.group(2) or match.group(3)

        s.result = s.find()

        if isinstance(s.result, s.i.unresolved): # ISSUE: Yet to implement in py interpreters
            s.match = match

    def multiInterpretS(s):
        value = s.ref[0]

        for match in re.finditer(s.i.allPatternString, value):
            print(match)
            skip = value[s.parsed:match.start()]
            s.parts.append(skip)

            result = s.interpretS(match) ###

            # container = s.ref[2]
            # script = Script(match.group(), "key", container, s.i) # ISSUE: change key later
            # script.process()
            # result = f"{script.result}" # ISSUE: Verify what types this returns

            if not isinstance(result, s.i.unresolved):
                s.parts.append(result)
            else:
                s.parts.append(match)

                if result.script.match:
                    identities = [id(result.script.trace(s.i.data))]
                else:
                    identities = list(result.script.awaiting.keys())
                    print(match, identities)

                for identity in identities:
                    if identity not in s.awaiting:
                        s.awaiting[identity] = []
                    s.awaiting[identity].append(len(s.parts) - 1)

            s.parsed = match.end()

            s.reset()

        skip = value[s.parsed:]
        s.parts.append(skip)

        if not s.awaiting:
            s.result = "".join(s.parts)
        else:
            s.result = s.i.unresolved(s)

    def interpretS(s, match):
        s.code = match.group()
        s.pre = match.group(1)

        if match.group(3):
            if match.group(5):
                if len(s.pre) % 2 == 1:
                    s.valid = False
                    return s.code[1:]
    
                s.pre = s.pre.replace(s.i.escape_*2, s.i.escape_)
    
                s.expression = match.group(5)

                result = s.interpret()

                if isinstance(result, s.i.unresolved):
                    return result

                return f"{s.pre}{result}"
            else:
                s.expression = match.group(6)
                result = s.retrieve()
    
                if s.valid:
                    if len(s.pre) % 2 == 1:
                        s.valid = False
                        return s.code[1:]
    
                    s.pre = s.pre.replace(s.i.escape_*2, s.i.escape_)
    
                    return f"{s.pre}{result}"
                else:
                    return f"{result}"
        elif match.group(7):
            s.expression = match.group(9) or match.group(10)
            result = s.find()

            if s.valid:
                if len(s.pre) % 2 == 1:
                    s.valid = False
                    return s.code[1:]

                if isinstance(result, s.i.unresolved):
                    return result
        
                s.pre = s.pre.replace(s.i.escape_*2, s.i.escape_)

                return f"{s.pre}{result}"
            else:
                return f"{result}"

    def interpret(s):
        s.expression = s.expression.replace(s.i.escape_+s.i.pygroup, s.i.pygroup)

        container = s.ref[2]
        script = Script(s.expression, "key", container, s.i) # ISSUE: change key later
        script.process()

        if isinstance(script.result, s.i.unresolved):
            return script.result

        s.expression = script.result # ISSUE: Verify what types this returns

        return s.evaluate()

    def retrieve(s):
        try:
            return s.evaluate()
        except NameError:
            s.valid = False
            return s.code

    def find(s):
        s.expression = s.expression.replace(s.i.escape_+s.i.objgroup, s.i.objgroup)

        try:
            result = s.trace(s.i.dataobject["data"])

            if not isinstance(result, s.i.unresolved):
                return result
            else:
                identity = id(s.trace(s.i.data))
                if identity not in s.awaiting:
                    s.awaiting[identity] = []
                s.awaiting[identity].append(None)
                # identity = id(s.trace(s.i.data))
                # if identity not in s.i.queue:
                #     s.i.queue[identity] = []
                # s.i.queue[identity].append(s) # ISSUE: Prevent multiple appends per listener

                return s.i.unresolved(s) # ISSUE: Do we need to re-create a new unreolved here, or use result's?
        except (KeyError, IndexError, ValueError):
            try:
                identity = id(s.trace(s.i.data))
                if identity not in s.awaiting:
                    s.awaiting[identity] = []
                s.awaiting[identity].append(None)
                # identity = id(s.trace(s.i.data))
                # if identity not in s.i.queue:
                #     s.i.queue[identity] = []
                # s.i.queue[identity].append(s)
    
                return s.i.unresolved(s)
            except (KeyError, IndexError, ValueError):
                s.valid = False
                return s.code

    def evaluate(s):
        return eval(s.expression, s.i.refs)

    def trace(s, source):
        track = s.expression.split(s.i.objsub)

        key = ""

        for n in range(len(track)):
            if len(re.search(s.i.escape + r'*$', track[n]).group()) % 2 == 1 and n + 1 < len(track):
                key += track[n] + s.i.objsub
                continue

            key += track[n]
            key = key.replace(s.i.escape_+s.i.objsub, s.i.objsub).replace(s.i.escape_*2, s.i.escape_)

            if isinstance(source, list):
                key = int(key)

            source = source[key]

            key = ""

        return source

    def queue(s):
        for identity in s.awaiting.keys():
            if identity not in s.i.queue:
                s.i.queue[identity] = []
            s.i.queue[identity].append(s)

    def announceresolved(s):
        value, key, container = s.ref[0], s.ref[1], s.ref[2]

        if not isinstance(container[key], s.i.unresolved):
            identity = id(value)

            if identity in s.i.queue:
                s.i.resolved.append(identity)