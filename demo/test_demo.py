# import pytest
#
#
# class TestDemo:
#     @classmethod
#     def setup_class(cls):
#         """ setup any state specific to the execution of the given class (which
#         usually contains tests).
#         """
#         with open('test.txt', 'w+') as f:
#             f.write('aaa')
#
#     @classmethod
#     def teardown_class(cls):
#         """ teardown any state that was previously setup with a call to
#         setup_class.
#         """
#         with open('./test.txt', 'a') as f:
#             f.write('ccc')
#
#     def test_answer(self):
#         with open('./test.txt', 'a') as f:
#             f.write('bbb')
#
#
# pytest.main()