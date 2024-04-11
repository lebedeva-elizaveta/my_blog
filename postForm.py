from wtforms import Form, StringField, DateTimeField


class PostForm(Form):
    title = StringField('Title')
    subtitle = StringField('Subtitle')
    author = StringField('Author')
    date_posted = DateTimeField('Date')
    content = StringField('Text')
