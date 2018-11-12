field_id = {
    'first_name': 0,
    'last_name': 1,
    'username': 2,
    'age': 3,
    'gender': 4,
    'city': 5
}


class Finder():

    def __init__(self, queries):
        self.queries = []
        if isinstance(queries, list):
            for query in queries:
                self.split_field(query)
        else:
            self.split_field(queries)

    def split_field(self, query):
        if query.get('where_and', ''):
            compare = Compare(query['where_and'], mode='and')
        elif query.get('where_or', ''):
            compare = Compare(query['where_or'], mode='or')
        else:
            compare = ''
        select = Select(query['select'], query.get('order', ''))
        self.queries.append({'compare': compare, 'select': select})

    def find(self, database):
        for query in self.queries:
            if query['compare']:
                query['compare'].find_match(database)
            else:
                query['select'].add_data(database)

    def show(self):
        for query in self.queries:
            if query['compare']:
                query['select'].add_data(query['compare'].valid_data)
            query['select'].show()


class Compare():

    def __init__(self, comparies, mode, field_id=field_id):
        self.comparies = comparies
        self.mode = mode
        self.fields = field_id
        self.valid_data = []

    def get_cond(self, key):
        return key['left'].split(' '), key['op'], key['right']

    def find_match(self, database, mode=''):
        for data in database:
            if self.check_match(data):
                self.valid_data.append(data)

    def check_match(self, data):
        for comp in self.comparies:
            pat, op, match = self.get_cond(comp)
            if self.mode == 'or' and self.is_match(pat, op, match, data):
                return True
            elif self.mode == 'and' and not self.is_match(pat, op, match, data):
                return False
        return True

    def is_match(self, pat, op, mat, data):
        if len(pat) > 1:
            field = pat[1]
            data = data[self.fields[field]][0]
        else:
            field = pat[0]
            data = data[self.fields[field]]
        if field == 'age':
            mat = int(mat)
        if field == 'gender':
            mat = mat.lower()
            data = data[: len(mat)]
        return ((op == '>' and data > mat) or
                (op == '<' and data < mat) or
                (op == '=' and data == mat) or
                (op == '!=' and data != mat))

    # def __repr__(self):
    #     data = [compare['left'] + " " + compare['op'] + " " +
    #             compare['right'] for compare in self.patterns]
    #     return " " + self.mode + "\n + " + "\n + ".join(data)


class Select():

    def __init__(self, field_show, order, fields=field_id):
        self.database = []
        self.fields_user = field_show.split(', ')
        self.order = order
        self.fields = fields

    def sort_data(self):
        if self.order:
            self.database = sorted(self.database, key=lambda k: (k[self.fields[self.order]]))

    def add_data(self, database):
        self.database = database
        self.sort_data()

    def show(self):
        for data in self.database:
            print(", ".join(map(str, self.get_field(data))))

    def get_field(self, data):
        return [data[self.fields[field]] for field in self.fields_user]

    # def __repr__(self):
    #     return "%s"%(", ".join(self.fields) + "\n" + "-Order: " +
    #                  self.order if self.order else ", ".join(self.fields)
    #                  +"\n" + "-Order: No")
