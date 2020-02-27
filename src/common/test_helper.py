from common.instance import db


def truncate_all():
    table_name_line = []
    result = db.session.execute('select tablename from pg_tables where schemaname = \'public\';')
    for row in result:
        table_name_line.append(row[0])
    db.session.execute('TRUNCATE TABLE {}'.format(', '.join(table_name_line)))
    db.session.commit()


class BaseTest:
    @classmethod
    def setup_class(cls):
        """ 类的测试运行之前 """
        db.create_all()
        truncate_all()

    # @classmethod
    # def teardown_class(cls):
    #     """ 类的测试运行之后 """
    #     db.session.remove()




if __name__ == '__main__':
    truncate_all()