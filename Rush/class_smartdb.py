field_id = {
    'first_name': 0,
    'last_name': 1,
    'username': 2,
    'age': 3,
    'gender': 4,
    'city': 5
}


class Smart_DB():

    def __init__(self, field_pattern=''):
        self.select = ""
        self.compare = ""
        self.field_pattern = field_pattern
        self.split_field()

    def split_field(self):
        if self.field_pattern.get('where_and', ''):
            self.compare = Compare(self.field_pattern['where_and'], mode='and')
        elif self.field_pattern.get('where_or', ''):
            self.compare = Compare(self.field_pattern['where_or'], mode='or')
        self.select = Select(self.field_pattern.get(
            'select', ''), self.field_pattern.get('order', ''))

    def find(self, database):
        if self.compare:
            self.compare.find_match(database)

    def show(self):
        if self.compare:
            self.select.get_data(self.compare.valid_data)
        else:
            self.select.get_data(database)
        self.select.show()


class Compare():
    valid_data = []

    def __init__(self, patterns, mode, field_id=field_id):
        self.patterns = patterns
        self.mode = mode
        self.field_id = field_id

    def get_pattern(self, key):
        return key['left'].split(' '), key['op'], key['right']

    def find_match(self, data):
        # for data in database:
        flag = True
        for comp in self.patterns:
            pattern, operator, match = self.get_pattern(comp)
            if self.mode == 'or' and self.is_matching(pattern,
                                                      operator,
                                                      match,
                                                      data):
                self.valid_data.append(data)
                break
            elif (self.mode == 'and' and
                  not self.is_matching(pattern,
                                       operator,
                                       match,
                                       data)):
                flag = False
                break
        if flag and self.mode == "and":
            self.valid_data.append(data)

    def is_matching(self, pattern, operator, match, data):
        if len(pattern) > 1:
            id = pattern[1]
            first = True
        else:
            id = pattern[0]
            first = False
        if id == 'age':
            match = int(match)
        if (first and
            ((operator == '>' and data[self.field_id[id]][0] > match) or
             (operator == '<' and data[self.field_id[id]][0] < match) or
             (operator == '=' and data[self.field_id[id]][0] == match) or
             (operator == '!=' and data[self.field_id[id]][0] != match))):
            return True
        elif (not first and
              ((operator == '>' and data[self.field_id[id]] > match) or
                (operator == '<' and data[self.field_id[id]] < match) or
                (operator == '=' and data[self.field_id[id]] == match) or
                (operator == '!=' and data[self.field_id[id]] != match))):
            return True
        return False

    def __repr__(self):
        data = [compare['left'] + " " + compare['op'] + " " +
                compare['right'] for compare in self.patterns]
        return " " + self.mode + "\n + " + "\n + ".join(data)


class Select():
    fields = []

    def __init__(self, field_show, order='', field_id=field_id):
        # stored field user wants
        for field in field_show.split(','):
            self.fields.append(field.strip())
        self.order = order
        self.field_id = field_id

    def get_data(self, database):
        if self.order:
            # sort data valid follow order
            self.valid_data = sorted(database, key=lambda k: (
                k[self.field_id[self.order]]))
        else:
            self.valid_data = database

    def show(self):
        for data in self.valid_data:
            # get field that user wants
            match = []
            for field in self.fields:
                match.append(str(data[self.field_id[field]]))
            print(", ".join(match))

    def __repr__(self):
        return "%s"%(", ".join(self.fields) + "\n" + "-Order: " +
                     self.order if self.order else ", ".join(self.fields) +
                     "\n" + "-Order: No")
