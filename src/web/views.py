from common.instance import app, db
# from missions.collection import LongTermBuy, ShortTermBuy, ShortTermSell
#
#
# @app.before_first_request
# def _init():
#     db.create_all()
#
#
# @app.route('/')
# def _detail():
#     line = ['<h2>长期策略</h2>']
#     line.extend(LongTermBuy().show_info())
#
#     line.append('<h2>短期策略</h2>')
#     line.extend(ShortTermBuy().show_info())
#
#     line.append('<h2>短期卖出策略</h2>')
#     line.extend(ShortTermSell().show_info())
#
#     result = '<br><br>'.join([str(i) for i in line])
#     result = result.replace('\n', '<br>')
#     return result


