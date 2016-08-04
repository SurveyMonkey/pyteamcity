class PageJoiner(object):
    def __init__(self, query_set):
        self.query_set = query_set
        self.num_items = 0

    @property
    def url(self):
        return self.query_set.url

    def __len__(self):
        return self.num_items

    def __iter__(self):
        data = self.query_set._data()
        while data.get('count') > 0:
            for x in self.query_set:
                yield x
                self.num_items += 1
            if 'nextHref' in data:
                self.query_set._data_dict = None
                data = self.query_set._data(href=data['nextHref'])
            else:
                break
