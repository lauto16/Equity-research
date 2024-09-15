import scraper
import cProfile


def mi_funcion():
    return sum([i for i in range(100000)])


# Perfilando el rendimiento
cProfile.run('scraper('','')', 'scraper.py')
