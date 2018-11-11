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
        self.querys = []
        if isinstance(field_pattern, list):
            for query in field_pattern:
                self.split_field(query)
        else:
            self.split_field(field_pattern)

    def split_field(self, query):
        compare = ''
        if query.get('where_and', ''):
            compare = Compare(query['where_and'], mode='and')
        elif query.get('where_or', ''):
            compare = Compare(query['where_or'], mode='or')
        select = Select(query['select'], query.get('order', ''))
        self.querys.append({'compare': compare, 'select': select})

    def find(self, database):
        for query in self.querys:
            if query['compare']:
                query['compare'].find_match(database)
            else:
                query['select'].add_data(database)

    def show(self):
        for query in self.querys:
            if query['compare']:
                query['select'].add_data(query['compare'].valid_data)
            query['select'].show()


class Compare():

    def __init__(self, patterns, mode, field_id=field_id):
        self.patterns = patterns
        self.mode = mode
        self.field_id = field_id
        self.valid_data = []

    def get_pattern(self, key):
        return key['left'].split(' '), key['op'], key['right']

    def find_match(self, data, mode="SINGLE"):
        # for data in database:
        flag = True
        if mode == 'SINGLE':
            self.check_match(data)
        else:
            for e in data:
                self.check_match(e)

    def check_match(self, data):
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
        if id == 'gender':
            if (match.upper() == 'M'):
                match = 'male'
            elif (match.upper() == 'F'):
                match = 'female'
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

    # def __repr__(self):
    #     data = [compare['left'] + " " + compare['op'] + " " +
    #             compare['right'] for compare in self.patterns]
    #     return " " + self.mode + "\n + " + "\n + ".join(data)


class Select():

    def __init__(self, field_show, order='', field_id=field_id):
        self.valid_data = []
        self.fields = []
        # stored field user wants
        for field in field_show.split(','):
            self.fields.append(field.strip())
        self.order = order
        self.field_id = field_id

    def sort_data(self):
        if self.order:
            # sort data valid follow order
            self.valid_data = sorted(self.valid_data, key=lambda k: (
                k[self.field_id[self.order]]))

    def add_data(self, database):
        if database:
            if isinstance(database[0], str):
                self.valid_data.append(database)
            else:
                self.valid_data += database

    def show(self):
        self.sort_data()
        for data in self.valid_data:
            # get field that user wants
            match = []
            for field in self.fields:
                match.append(str(data[self.field_id[field]]))
            print(", ".join(match))

    # def __repr__(self):
    #     return "%s"%(", ".join(self.fields) + "\n" + "-Order: " +
    #                  self.order if self.order else ", ".join(self.fields)
    #                  +"\n" + "-Order: No")
