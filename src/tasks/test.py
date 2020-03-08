from datetime import datetime
from uuid import uuid4 as uuid

from common.instance import db
from common.test_helper import BaseTest, truncate_all
from configs import TIMEZONE
from tasks.template.base import TaskTemplateBase


class Test(BaseTest):
    def test_get_args(self):
        """ 测试 task template base能不能正确返回自己try pass的参数"""
        class TempClass(TaskTemplateBase):
            def try_pass(self, size, match):
                return True

        result = TempClass.get_args()
        assert result[0] == 'size'
        assert result[1] == 'match'


if __name__ == '__main__':
    import pytest
    pytest.main(['./test.py'])