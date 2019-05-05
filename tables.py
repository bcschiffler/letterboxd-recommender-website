from flask_table import Table, Col

class ImageCol(Col):
    def td_format(self, content):
        val = '<img src=' + content + '>'
        return f'{val}'

class UrlCol(Col):
    def td_format(self, content):
        val = '<a href=https://letterboxd.com' + content + ' target="_blank">Link</a>'
        return f'{val}'

class Results(Table):
    #id = Col('id', show=False)
    #user_id = Col('user_id')
    #col_type = Col('col_type')
    #movie_id = Col('movie_id')
    #info = Col('info')
    name = Col('name')
    image_src = ImageCol('image_src')
    path = UrlCol('path')