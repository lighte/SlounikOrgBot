from collections import OrderedDict

class HtmlCache:
    def __init__(self, max_size=10000):
        self.cache = OrderedDict()
        self.max_size = max_size

    def cached(self, query: str, getter) -> list[str]:
        if query in self.cache:
            # Move the key to the end to mark it as recently used
            self.cache.move_to_end(query)
            return self.cache[query]
        
        # Cache miss: call getter
        result = getter(query)

        # Insert into cache
        self.cache[query] = result

        # Evict oldest item if over size
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)  # Pop the least recently used item

        return result