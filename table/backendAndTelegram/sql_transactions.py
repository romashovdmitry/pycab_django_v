from sqlalchemy import create_engine


class SQLTransactions():

    db = create_engine(
        'postgresql://postgres:polkabulok56@pgdb:5432/pycab_django_db')
    conn = db.connect()

    def __init__(self, telegram_id=None, user_level=None, user_email=None,
                 message=None, status_of_word_in_whole=None,
                 word_in_whole=None, definition=None, highest=None,
                 status_of_word_in_dynamic=None, id_of_word_in_dynamic=None,
                 rownumber=None, word_in_dynamic=None, password=None):

        self.word_in_whole = word_in_whole
        self.telegram_id = telegram_id
        self.user_level = user_level
        self.password = password
        self.user_email = user_email
        self.message = message
        self.status_of_word_in_whole = status_of_word_in_whole
        self.definition = definition
        self.highest = highest
        self.status_of_word_in_dynamic = status_of_word_in_dynamic
        self.id_of_word_in_dynamic = id_of_word_in_dynamic
        self.rownumber = rownumber
        self.word_in_dynamic = word_in_dynamic

    '''
    Foo checks is there telegram_id in table users or not, i.e. user is
    authorized or not in Telegram Bot.

    '''

#   if UserInfo.objects.filter(telegram_id=telegram_id).first().user_level is not None:
    def validateLevel(self):
        db_answer = self.db.execute("SELECT user_level FROM table_userinfo "
                                    "WHERE telegram_id={};".
                                    format(self.telegram_id)).first()
        return False if db_answer is None else True

    def validateUserInTable(self):
        print('i am here in DB')
        db_answer = self.db.execute(
            "select TRUE HAVING {} IN ("
            "SELECT telegram_id FROM table_userinfo);".format(self.telegram_id)).first()
        return False if db_answer is None else True

# MyUser.objects.filter(email=em).exists()
    def validateEmailInTable(self):
        db_answer = self.db.execute(
            "select TRUE HAVING '{}' IN ("
            "SELECT email FROM table_myuser);".
            format(self.user_email)).first()
        return False if db_answer is None else True


    def updateUserLevel(self):
        self.db.execute("UPDATE table_userinfo "
                        "SET user_level = '{}' "
                        "WHERE user_email_id='{}';"
                        .format(self.user_level,
                                self.user_email))

#   user_info = UserInfo.objects.get(telegram_id=telegram_id)
#   user_info.user_level='start password'
#   user_info.save()
    def setTelegramIdByEmail(self):
        self.db.execute("UPDATE table_userinfo\
                    SET telegram_id={}, user_level='start password'\
                    WHERE user_email_id='{}';\
                    ".format(self.telegram_id, self.user_email))


#   email_of_user = UserInfo.objects.filter(telegram_id=telegram_id).first().user_email
    def findUserEmailByTelegramId(self):
        return self.db.execute("SELECT user_email_id "
                               "FROM table_userinfo "
                               "WHERE telegram_id={};"
                               .format(self.telegram_id)).first(
                                                )['user_email_id']

    def findPasswordByTelegramId(self):
        return self.db.execute("SELECT password "
                               "FROM table_myuser mu "
                               "JOIN table_userinfo ui "
                               "ON mu.email=ui.user_email_id "
                               "WHERE ui.telegram_id={};".
                               format(self.telegram_id)).first()[
                                                        'password']

    def deleteAllFromDynamicByEmail(self):
        self.db.execute("DELETE FROM table_dynamicvocab "
                        "WHERE user_email_id='{}';".format(self.user_email))

    def updateWordByPk(self):
        self.db.execute("UPDATE table_wholevocab "
                        "SET word_in_whole='{}' "
                        "WHERE id_of_word_in_whole={};".
                        format(self.word_in_whole, self.rownumber))

# vocab_string = WholeVocab.objects.filter(id_of_word_in_whole=session_pk).first()
#            vocab_string.update_string(
#                word=word,
#                definition=definition
#            )

    def updateWordDefinitionInWhole(self):
        self.db.execute("UPDATE table_wholevocab "
                        "SET word_in_whole='{}', "
                        "definition_of_word_in_whole='{}' "
                        "WHERE id_of_word_in_whole={};".
                        format(self.word_in_whole, self.definition,
                               self.rownumber))

#    def add_new_string(self, email, word, definition):
#        self.word_in_whole = word
#        self.definition_of_word_in_whole = definition
#        self.user_email = email
#        self.save()
    def addWordDefinitionInWhole(self):
        self.db.execute("INSERT INTO table_wholevocab "
                        "(word_in_whole, definition_of_word_in_whole, "
                        "user_email_id) "
                        "VALUES ('{}', '{}', '{}');".
                        format(self.word_in_whole, self.definition,
                               self.user_email))

#   records = WholeVocab.objects.filter(user_email=email_adress).all()
    def selectAllInWholeVocabByEmail(self):
        return self.db.execute("SELECT * FROM table_wholevocab "
                               "WHERE user_email_id='{}';"
                               .format(self.user_email)).fetchall()

    def findUserLevelByTelegramId(self):
        return self.db.execute("SELECT user_level "
                               "FROM table_userinfo "
                               "WHERE telegram_id={};"
                               .format(self.telegram_id)).first()['user_level']

    def copyRecordsFromWholeToDynamic(self):
        self.db.execute("INSERT INTO table_dynamicvocab "
                        "(user_email_id, word_in_dynamic, "
                        "definition_in_dynamic, id_of_word_in_dynamic_id)"
                        " SELECT user_email_id, word_in_whole, "
                        "definition_of_word_in_whole, "
                        "id_of_word_in_whole "
                        "FROM table_wholevocab WHERE user_email_id='{}';".
                        format(self.user_email))

    def selectAllWordsFromWhole(self):
        return self.db.execute("SELECT word_in_whole "
                               "FROM table_wholevocab "
                               "WHERE user_email_id='{}';".
                               format(self.user_email))

    def selectAllWordsFromDynamic(self):
        return self.db.execute("SELECT word_in_dynamic "
                               "FROM table_dynamicvocab "
                               "WHERE user_email_id='{}';".
                               format(self.user_email))

    def selectAllRecordsFromDynamic(self):
        return self.db.execute("SELECT * "
                               "FROM table_dynamicvocab "
                               "WHERE user_email_id='{}';".
                               format(self.user_email))

    def selectPkeysFromDynamic(self):
        return self.db.execute("SELECT id_of_word_in_dynamic_id "
                               "FROM table_dynamicvocab "
                               "WHERE user_email_id='{}';".
                               format(self.user_email)).fetchall()

    def selectDynamicDoing(self):
        return self.db.execute("SELECT definition_in_dynamic "
                               "FROM table_dynamicvocab "
                               "WHERE status_of_word_in_dynamic='doing' "
                               "AND user_email_id='{}';".
                               format(self.user_email)
                               ).first()['definition_in_dynamic']

    def selectDynamicModif(self):
        return self.db.execute("SELECT definition_in_dynamic "
                               "FROM table_dynamicvocab "
                               "WHERE status_of_word_in_dynamic='modif' "
                               "AND user_email_id='{}';".
                               format(self.user_email)
                               ).first()['definition_in_dynamic']

    def setStatudInDynamic(self):
        self.db.execute("UPDATE table_dynamicvocab "
                        "SET status_of_word_in_dynamic='{}' "
                        "WHERE user_email_id='{}' "
                        "AND id_of_word_in_dynamic_id={};".
                        format(self.status_of_word_in_dynamic,
                               self.user_email,
                               self.id_of_word_in_dynamic))

    def setStatusInDynamicModif(self):
        self.db.execute("UPDATE table_dynamicvocab "
                        "SET status_of_word_in_dynamic='modif' "
                        "WHERE word_in_dynamic='{}' "
                        "AND user_email_id='{}';".
                        format(self.word_in_dynamic,
                               self.user_email))

    def selectDynamicDefenitionStatusDoing(self):
        self.db.execute("SELECT definition_in_dynamic "
                        "FROM table_dynamicvocab "
                        "WHERE status_of_word_in_dynamic='{}' "
                        "AND user_email_id='{}';".
                        format(self.status_of_word_in_dynamic,
                               self.user_email))

    def updateAllStatusInWhole(self):
        self.db.execute("UPDATE table_wholevocab "
                        "SET status_of_word_in_whole='not done' "
                        "WHERE user_email_id='{}';".
                        format(self.user_email))

    def insertWordInWhole(self):
        self.db.execute("INSERT INTO table_wholevocab"
                        "(word_in_whole, user_email_id, "
                        "status_of_word_in_whole)"
                        "VALUES('{}', '{}', '{}');".
                        format(self.word_in_whole,
                               self.user_email,
                               self.status_of_word_in_whole))

    def insertDefinitionInWhole(self):
        self.db.execute("UPDATE table_wholevocab "
                        "SET definition_of_word_in_whole='{}' "
                        "WHERE status_of_word_in_whole='doing' "
                        "AND user_email_id='{}';".
                        format(self.definition,
                               self.user_email))

    def findWordDynamicStatusDoing(self):
        return self.db.execute("SELECT word_in_dynamic "
                               "FROM table_dynamicvocab "
                               "WHERE status_of_word_in_dynamic='doing' "
                               "AND user_email_id='{}';".
                               format(self.user_email)).first()[
                                            'word_in_dynamic']

    def deleteRecordDynamicStatusDoing(self):
        self.db.execute("DELETE FROM table_dynamicvocab "
                        "WHERE status_of_word_in_dynamic='doing' "
                        "AND user_email_id='{}';".
                        format(self.user_email))

    def deleteRecordWholeByWord(self):
        self.db.execute("DELETE FROM table_wholevocab "
                        "WHERE word_in_whole='{}' "
                        "AND user_email_id='{}';".
                        format(self.word_in_whole,
                               self.user_email))

    def deleteRecordWholeByPkey(self):
        self.db.execute("DELETE FROM table_wholevocab "
                        "WHERE id_of_word_in_whole={};".
                        format(self.rownumber))
#
#
#
    def getWordFromWhole(self):
        return self.db.execute("SELECT word_in_whole "
                               "FROM table_wholevocab "
                               "WHERE id_of_word_in_whole={};".
                               format(self.rownumber)).first()['word_in_whole']

    def getDefinitionWholeByPK(self):
        return self.db.execute("SELECT definition_of_word_in_whole "
                               "FROM table_wholevocab "
                               "WHERE id_of_word_in_whole={};".
                               format(self.rownumber)).first()[
                                'definition_of_word_in_whole']

    def findRecordPkeyStatusModif(self):
        return self.db.execute("SELECT id_of_word_in_dynamic_id "
                               "FROM table_dynamicvocab "
                               "WHERE user_email_id='{}' "
                               "AND status_of_word_in_dynamic='modif';".
                               format(self.user_email)).first(
                                    )['id_of_word_in_dynamic_id']

    def updateDefinitionInWhole(self):
        self.db.execute("UPDATE table_wholevocab "
                        "SET definition_of_word_in_whole='{}'"
                        "WHERE id_of_word_in_whole={};".format(
                            self.definition,
                            self.id_of_word_in_dynamic))

    def updateStatusModifInDynamic(self):
        self.db.execute("UPDATE table_dynamicvocab "
                        "SET status_of_word_in_dynamic='modif' "
                        "WHERE id_of_word_in_dynamic_id={};"
                        .format(self.rownumber))
#   password = MyUser.objects.filter(email=em).first().password
    def getPasswordOfUser(self):
        return self.db.execute("SELECT password "
                               "FROM table_myuser "
                               "WHERE email='{}';".
                               format(self.user_email)).first()['password']


#   user = MyUser.objects.get(email=em)
#   user.password = new_password
#   user.save()
    def setNewPassword(self):
        self.db.execute("UPDATE table_myuser "
                        "SET password='{}' "
                        "WHERE email='{}';".
                        format(self.password, self.user_email))
