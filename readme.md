# ПРАВА АДМИНИСТРАТОРА

# 1. Новый пользователь (через Python Console)

~~~python
from app import *
u = User(email = '*****', password = '******')
r = Role(name = 'admin')
u.roles.append(r)
db.session.add(u)
db.session.commit()
~~~

# 2. Зарегистрированный пользователь (через Python Console)

~~~python
from app import *
u = User.query.filter(User.email == '*****').first()
r = Role(name = 'admin')
u.roles.append(r)
db.session.add(u)
db.session.commit()
~~~