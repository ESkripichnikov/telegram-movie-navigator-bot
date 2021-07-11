class NoMoviesError(Exception):
    def __str__(self):
        return "The list of movies is empty!"
