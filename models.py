from peewee import *
import api_wrapper
from time import time as curr_time
from json import loads

database = SqliteDatabase('user.db')

# == DEV ==
#api = api_wrapper.CryptaKingsAPI()
import uuid

# == DEV ==

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    user_id_tg = CharField(unique=True)
    created_tg = FloatField(default=curr_time)
    logged_in = BooleanField(default=False)

    created = TextField(null=True)
    _id = TextField(null=True)
    first_name = TextField(default='')
    last_name = TextField(default='')
    
    rank = IntegerField(null=True)
    performance = IntegerField(null=True)

    def get_following(self):
        return (Trader
                .select()
                .join(Relationship, on=Relationship.to_user)
                .where(Relationship.from_user == self)
                .order_by(Trader.rank))

    def is_following(self, trader):
        return (Relationship
                .select()
                .where(
                    (Relationship.from_user == self) &
                    (Relationship.to_user == trader))
                .exists())

    def refresh_token(self):
        return get_object(self.token).refresh()

    def delete_token(self):
        try:
            Token.delete().where((Token.user == self)).execute()
        except:
            raise

    def reset_info(self):
        self.created = None
        self._id = None
        self.first_name = ''
        self.last_name = ''
        self.save()

    def login(self, username, password):
        if self.logged_in:
            return False
        self.get_token(username, password)
        self.logged_in = True
        self.save()
        return True

    def logout(self):
        if self.logged_in:
            self.delete_token()
            self.logged_in = False
            self.save()
            return True
        return False      

    def get_token(self, username, password):

        #response = loads(api.auth_get_token(username, password))
        response = {'access_token': uuid.uuid4(),
                    'refresh_token': uuid.uuid4(),
                    'expires_in': 60}
        
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_in = response['expires_in']

        with database:
            token = Token.create(
                user=self,
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires=curr_time() + expires_in) 
        return token

    def get_transactions(self):
        
        token = get_object(self.token)
        if not token:
            token = self.get_token()
        else:
            if token.is_expired():
                token = self.refresh_token()

        # TODO API REQUEST get_transactions
        print(self.user_id_tg, 'requested his transactions')
        return ['12', '12312', 'asd']

        
        
class Token(BaseModel):
    user = ForeignKeyField(User, backref='token', unique=True)
    access_token = CharField()
    refresh_token = CharField()
    token_expires = IntegerField()

    def is_expired(self):
        if curr_time() < self.token_expires:
            return False
        else:
            return True

    def refresh(self):

        #response = loads(api.auth_refresh_token(self.refresh_token))
        response = {'access_token': uuid.uuid4(),
                    'refresh_token': uuid.uuid4(),
                    'expires_in': 60}
        
        with database.atomic():
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            self.expires_in = curr_time() + response['expires_in']
            self.save()
        return self

class Trader(BaseModel):
    
    _id = TextField(unique=True)
    first_name = TextField()
    last_name = TextField()

    rank = IntegerField()
    performance = IntegerField()

    def get_transactions(self):
        return ['1', '2', '3']

    def get_followers(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.from_user)
                .where(Relationship.to_user == self))

class Relationship(BaseModel):
    to_user = ForeignKeyField(Trader, backref='subscribers')
    from_user = ForeignKeyField(User, backref='subscripted_to')
    class Meta:
        indexes = ((('from_user', 'to_user'), True),)
        
def create_tables():
    with database:
        database.create_tables([User, Relationship, Token, Trader], safe=True)

def get_object(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        return None

def new_user(user_id_tg):
    try:
        with database.atomic():
            user = User.create(user_id_tg=user_id_tg)
    except IntegrityError:
        raise
    else:
        return user

def get_user_tg(user_id_tg):
    return get_object(User, User.user_id_tg == user_id_tg)

def get_user_id(_id):
    return get_object(User, User._id == _id)

def user_follow(user_id_id, trader_id):
    trader = get_object(Trader, Trader._id == trader_id)
    user = get_user_tg(user_id_tg)
    try:
        with database.atomic():
            Relationship.create(
                from_user=user,
                to_user=trader)
    except IntegrityError:
        raise

def user_unfollow(user_id_tg, trader_id):
    trader = get_object(Trader, Trader._id == trader_id)
    user = get_user_tg(user_id_tg)
    try:
        with database.atomic():
            (Relationship
             .delete()
             .where(
                 (Relationship.from_user == user) &
                 (Relationship.to_user == trader))
             .execute())
    except IntegrityError:
        raise

def user_list():
    users = User.select().order_by(User.rank)
